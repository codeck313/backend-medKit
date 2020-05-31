import paho.mqtt.client as mqtt

broker_address = "127.0.0.1"

client = mqtt.Client("DEV1")
client.connect(broker_address, 1883, 60)
client.publish("1_2/Details", "123478,Sharma,20,M")
client.publish("1_1/Details", "124558,Saksham Sharma,20,M,15")
client.publish("1_3/Details", "124558,Saksham Sharma,20,M,15")
# client.publish("1_1/Temp", "25,26.7")
# client.publish("1_1/HeartRate", "78.5,58.7")
# client.publish("1_1/SpO2", "80,78.8")
# client.publish("1_1/BP", "58,68")

# client.publish("1_2/Temp", "25,26.7")
# client.publish("1_2/HeartRate", "78.5,58.7")
# client.publish("1_2/SpO2", "80,78.8")
# client.publish("1_2/BP", "58,68")
