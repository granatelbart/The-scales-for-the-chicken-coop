#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import gpiozero
import time
from gpiozero import DigitalOutputDevice
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
################################################################


class HP4067Mux:
    def __init__(self, s0, s1, s2, s3):
        """
        Arguments s0 to s3 represent the address input as in the datasheet
        """
        self._outs = [DigitalOutputDevice(pin=pin) for pin in [s0, s1, s2, s3]]
        self.channel(0)
    def channel(self, value):
        """
        Select the muxed channel from 0 to 15
        """
        assert 0 <= value <= 15, "Can only mux 4 lines"
        for i, pin in enumerate(self._outs):
            pin.value = bool(1 << i & value)


mymux = HP4067Mux(19,6,5,12)
mymux.channel(0)

####################################################################

reader = SimpleMFRC522()

while True:
   # GPIO.cleanup()
    try:
        id, name = reader.read()
 
        print(id)
        print(name)
        
        time.sleep(2) 

    except KeyboardInterrupt:
        pass  # User can end this with Ctrl+C.
    finally:
        print("Cleaning...")
        GPIO.cleanup()
        print("Bye!")
