import paho.mqtt.client as mqtt
import sqlite3
import datetime

broker_address = "127.0.0.1"
dataToPush = {}
changed = []
idToSub = ["123458", "123358", "123558",
           "123758", "123158", "123858", "124558"]


def subToChannel(id):
    client.subscribe(id+"/Details")
    client.subscribe(id+"/Temp")
    client.subscribe(id+"/HeartRate")
    client.subscribe(id+"/BP")
    client.subscribe(id+"/SpO2")


def subToChannels(channels):
    for channel in channels:
        subToChannel(channel)


def createTable(db):
    cursorDb = db.cursor()
    cursorDb.execute(
        "CREATE TABLE IF NOT EXISTS patient(id integer PRIMARY KEY,Name text NOT NULL,Age integer,Sex text,BedNo integer);")
    cursorDb.execute(
        "CREATE TABLE IF NOT EXISTS medicData(id integer ,Time text,tempCurrent real,tempAvg real,bpmCurrent real,bpmAvg real,bpCurrent real,bpAvg real,spO2Current real,spO2Avg real);")
    db.commit()
    cursorDb.close()


def newPatient(db, details):
    cursorDb = db.cursor()
    cursorDb.execute(
        "INSERT OR REPLACE INTO patient(id, Name, Age, Sex, BedNo) VALUES({},'{}',{},'{}',{});".format(details[0], details[1], details[2], details[3], details[4]))
    db.commit()
    cursorDb.close()


def pushData(db):
    # ID,Time,Archived,CurrentTemp,AvgTemp
    # datetime.datetime.now()
    global changed
    global dataToPush
    cursorDb = db.cursor()
    for changedId in changed:
        command = """INSERT INTO medicData(id, Time, tempCurrent, tempAvg,
            bpmCurrent, bpmAvg, bpCurrent, bpAvg, spO2Current, spO2Avg)
            VALUES({},"{}",{},{},{},{},{},{},{},{});""".format(changedId, datetime.datetime.now(),
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
        searchParam)
    cursorDb.execute(command)
    return cursorDb.fetchall()[0]


def addToDict(payload, changed, data, db):
    deviceID = str(payload.topic).split("/")[0]
    parameter = str(payload.topic).split("/")[1]
    message = str(payload.payload.decode("utf-8")).split(",")
    if data.get(deviceID) == None:
        data[deviceID] = {}
        changed.append(deviceID)
    if (parameter == "Details"):
        # Name,Age,Sex,BedNo
        newPatient(db, [deviceID, message[0],
                        message[1], message[2], message[3]])
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
    print("message received ", str(message.payload.decode("utf-8")).split(","))
    print("message topic=", str(message.topic).split("/")[1])
    addToDict(message, changed, dataToPush, dataBase)
    print("Changed: ", changed)
    print("DataFrame: ", dataToPush)


dataBase = sqlite3.connect('patientInfo.db')
createTable(dataBase)
client = mqtt.Client("baseStation")
client.connect(broker_address, 1883, 60)
subToChannels(idToSub)
client.on_message = on_message
while(1):
    client.loop()
    pullRecord(dataBase, "123458")
    try:
        pushData(dataBase)
    except KeyError:
        print("DataIncomplete")

    # time.sleep(5)
