#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
from mfrc522 import SimpleMFRC522
import array as arr

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pinList = [5,24,0,2,3,4,27,25]
rfidList = [1081714680121,871849641659,504025229752,275844158012,648722309022,118668796333,737282492797]
id  = 0

while True:
    reader = SimpleMFRC522()
    id, text = reader.read()
    print(id)
    if id:
        if id == 828191200458:
            for i in pinList:
                os.system("sudo gpio mode "+str(i)+" out")
            time.sleep(0.5)

            for i in pinList:
                os.system("sudo gpio mode "+str(i)+" in")
            time.sleep(0.5)

        for i in range(len(rfidList)):
            if id == rfidList[i]:
                os.system("sudo gpio mode "+str(pinList[i])+" out")
            time.sleep(3.5)
            os.system("sudo gpio mode "+str(pinList[i])+" in")
    GPIO.cleanup()
    time.sleep(0.5)
