import paho.mqtt.client as mqtt
import sqlite3
import datetime

broker_address = "127.0.0.1"
dataToPush = {}
changed = []
bedToSub = []
bedToId = {}  # lookup dict


def getBeds(db):
    """
    Populate the bedToSub list from the db
    """
    global bedToSub
    cursorDb = db.cursor()
    command = "SELECT WardNo, BedNo FROM patient;"
    cursorDb.execute(command)
    for element in cursorDb.fetchall():
        out = str(element[0])+"_"+str(element[1])
        bedToSub.append(out)
    bedToSub = list(dict.fromkeys(bedToSub))
    print(bedToSub)


def getPatientID(db, key):
    """
    provide the latest patient id for respective bedNo and wardNo
    """
    # (SELECT * FROM medicData ORDER BY Time DESC) WHERE id = {} LIMIT 1;"
    global bedToId
    if bedToId.get(key, None) == None:
        cursorDb = db.cursor()
        command = "SELECT id FROM patient WHERE BedNo = {} AND WardNo = {};".format(
            key.split("_")[1], key.split("_")[0])
        cursorDb.execute(command)
        bedToId[key] = cursorDb.fetchall()[0][-1]
    return bedToId[key]


def subToChannel(id):
    print("Sub to", id)
    client.subscribe(id+"/Details")
    client.subscribe(id+"/Temp")
    client.subscribe(id+"/HeartRate")
    client.subscribe(id+"/BP")
    client.subscribe(id+"/SpO2")


def subToChannels(channels):
    """
    Using subToChannel Subscribe to all the mqtt topics
    """
    for channel in channels:
        subToChannel(channel)


def createTable(db):
    """
    Iinitialize the DB
    """
    cursorDb = db.cursor()
    cursorDb.execute(
        "CREATE TABLE IF NOT EXISTS patient(id integer PRIMARY KEY,Name text NOT NULL,Age integer,Sex text,BedNo integer,WardNo integer,Time text);")
    cursorDb.execute(
        "CREATE TABLE IF NOT EXISTS medicData(id integer ,Time text,tempCurrent real,tempAvg real,bpmCurrent real,bpmAvg real,bpCurrent real,bpAvg real,spO2Current real,spO2Avg real);")
    db.commit()
    cursorDb.close()


def newPatient(db, details):
    """
    Insert New patient details into DB
    """
    print("Adding patient", details, datetime.datetime.now())
    cursorDb = db.cursor()
    cursorDb.execute(
        "INSERT OR REPLACE INTO patient(id, Name, Age, Sex, BedNo,WardNo,Time) VALUES({},'{}',{},'{}',{},{},'{}');".format(details[0], details[1], details[2], details[3], details[4], details[5], datetime.datetime.now()))
    db.commit()
    cursorDb.close()
    global bedToSub
    out = str(details[5])+"_"+str(details[4])
    bedToSub.append(out)
    bedToSub = list(dict.fromkeys(bedToSub))
    subToChannel(out)
    print(bedToSub)


def pushData(db):
    """
    Push data to medicTable
    """
    # ID,Time,Archived,CurrentTemp,AvgTemp
    global changed
    global dataToPush
    cursorDb = db.cursor()
    for changedId in changed:
        command = """INSERT INTO medicData(id, Time, tempCurrent, tempAvg,
            bpmCurrent, bpmAvg, bpCurrent, bpAvg, spO2Current, spO2Avg)
            VALUES({},"{}",{},{},{},{},{},{},{},{});""".format(getPatientID(db, changedId), datetime.datetime.now(),
                                                               dataToPush[changedId]["temp"][0], dataToPush[changedId]["temp"][1],
                                                               dataToPush[changedId]["heartRate"][0], dataToPush[changedId]["heartRate"][1],
                                                               dataToPush[changedId]["BP"][0], dataToPush[changedId]["BP"][1],
                                                               dataToPush[changedId]["SpO2"][0], dataToPush[changedId]["SpO2"][1])
        print("SQLITE COMMAND", command)
        cursorDb.execute(command)
        dataToPush[changedId] = None
        changed.remove(changedId)
    db.commit()
    cursorDb.close()


def pullRecord(db, searchParam):
    cursorDb = db.cursor()
    command = "SELECT * FROM (SELECT * FROM medicData ORDER BY Time DESC) WHERE id = {} LIMIT 1;".format(
        getPatientID(db, searchParam))
    cursorDb.execute(command)
    return cursorDb.fetchall()[0]


def addToDict(payload, changed, data, db):
    """
    Append the latest readings of the patient into the dictionary
    """
    deviceID = str(payload.topic).split("/")[0]
    parameter = str(payload.topic).split("/")[1]
    message = str(payload.payload.decode("utf-8")).split(",")
    if data.get(deviceID) == None:
        data[deviceID] = {}
        changed.append(deviceID)
    if (parameter == "Details"):
        # id, Name, Age, Sex, BedNo,WardNo
        newPatient(db, [message[0],
                        message[1], message[2], message[3], deviceID.split("_")[1], deviceID.split("_")[0]])
    if(parameter == "Temp"):
        # current Reading , Avg Reading
        data[deviceID]["temp"] = [float(message[0]), float(message[1])]
    if(parameter == "HeartRate"):
        data[deviceID]["heartRate"] = [float(message[0]), float(message[1])]
    if(parameter == "BP"):
        data[deviceID]["BP"] = [float(message[0]), float(message[1])]
    if(parameter == "SpO2"):
        data[deviceID]["SpO2"] = [float(message[0]), float(message[1])]
    # message = str(payload.payload.decode("utf-8")).split(",")


def on_message(client, userdata, message):
    global changed
    # print("message received ", str(message.payload.decode("utf-8")).split(","))
    # print("message topic=", str(message.topic).split("/")[1])
    addToDict(message, changed, dataToPush, dataBase)
    print("Changed: ", changed)
    print("DataFrame: ", dataToPush)


dataBase = sqlite3.connect('patientInfo.db')
createTable(dataBase)
client = mqtt.Client("baseStation")
client.connect(broker_address, 1883, 60)
getBeds(dataBase)
subToChannels(bedToSub)
client.on_message = on_message
while(1):
    client.loop()
    # print(pullRecord(dataBase, "1_2"))
    try:
        pushData(dataBase)
    except KeyError as e:
        pass
        # print(e)
        # print("DataIncomplete")

# time.sleep(5)
