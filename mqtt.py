#mqtt.py

import time
import paho.mqtt.client as mqtt
import sensor

flag = False


broker_ip ="localhost"
client = mqtt.Client()

client.connect(broker_ip, 1883)
client.loop_start()

def on_connect(client, userdata, flag, rc):
        client.subscribe("face", qos = 0)

def on_message(client, userdata, msg) :
        global flag
        command = msg.payload.decode("utf-8")
        if command == "action" :
                print("action msg received..")
                flag = True

client.on_connect = on_connect
client.on_message = on_message



while True:
        light = sensor.getLight()
        client.publish("light",light,qos=0)
        distance = sensor.measureDistance()
        client.publish("distance",distance,qos=0)
        if distance >= 15:
                sensor.ledOut()
                sensor.SpeakerOff()
                client.publish("safe",1,qos=0)
                imageFileName = sensor.takePicture()
                client.publish("image",imageFileName,qos=0)
        else:
                sensor.ledIn()
                sensor.Speaker()
                imageFileName = sensor.takePicture()
                client.publish("image",imageFileName,qos=0)
        time.sleep(0.1)
print("time...",end=" ")
print(flag)
client.loop_end()
client.disconnect()
