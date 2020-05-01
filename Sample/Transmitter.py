import paho.mqtt.client as mqtt

broker_address = "127.0.0.1"

client = mqtt.Client("DEV1")
client.connect(broker_address, 1883, 60)
# client.publish("123458/Details", "Saksham Sharma,20,M,15")
# client.publish("123358/Details", "Saksham Sharma,20,M,15")
# client.publish("123558/Details", "Saksham Sharma,20,M,15")
# client.publish("123758/Details", "Saksham Sharma,20,M,15")
# client.publish("123158/Details", "Saksham Sharma,20,M,15")
# client.publish("123858/Details", "Saksham Sharma,20,M,15")
# client.publish("124558/Details", "Saksham Sharma,20,M,15")
client.publish("123458/Temp", "25,26.7")
client.publish("123458/HeartRate", "78.5,58.7")
client.publish("123458/SpO2", "80,78.8")
client.publish("123458/BP", "58,68")
