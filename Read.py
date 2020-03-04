#!/usr/bin/env python
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import os
import time
from mfrc522 import SimpleMFRC522

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

reader = SimpleMFRC522()

#try:
#       name= reader.read()
#        print(name)
#        #print(alter)
#        #print(impfung)
#        #client.publish("huhn/name", name)
#finally:
#        GPIO.cleanup()

GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
pinList = [22,24,19,21,23]
rfidList = [1081714680121,871849641659,504025229752,275844158012,648722309022,118668796333,737282492797]

while True:
    reader = SimpleMFRC522()
    id, name = reader.read()
    client.publish("name/reader", name)
    time.sleep(0.5)
#except KeyboardInterrupt:
#    pass  # User can end this with Ctrl+C.
