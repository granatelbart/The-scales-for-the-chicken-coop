#! /usr/bin/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO #allgemeines Einbinden der GPIO-Funktion 
import time
import subprocess
import lcddriver

lcd = lcddriver.lcd()

GPIO.setmode(GPIO.BCM) #Zählweise der GPIO-PINS auf der Platine, analog zu allen Beispielen
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Taster ist an GPIO-Pin 23 angeschlossen 
while True:
    input_state = GPIO.input(23)
    if input_state == False:
        print ("RasPi Neustart")
        lcd.lcd_clear()
        time.sleep(3.2)
        lcd.lcd_display_string("Good Bye", 3)
        time.sleep(3.2)
        lcd.lcd_display_string("Neustart", 4)
        time.sleep(3.2)
        subprocess.call(['shutdown', '-r', 'now'], shell=False)
        time.sleep(0.2)
