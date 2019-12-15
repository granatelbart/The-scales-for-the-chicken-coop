#! /usr/bin/python3
# -*- coding: utf-8 -*-

import time
import sys
import lcddriver 
import RPi.GPIO as GPIO
import math

GPIO.setmode(GPIO.BCM) #Zählweise der GPIO-PINS auf der Platine, analog zu allen Beispielen
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Taster ist an GPIO-Pin 23 angeschlossen

#Schnittstellenbeschreibung
lcd = lcddriver.lcd()                            #LCD

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(343)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")
lcd.lcd_display_string("Waage gestartet", 4)
time.sleep(5.2)

while True:
    input_state = GPIO.input(25)
    if input_state == False:
        print("Tara ausgeführt")
        lcd.lcd_display_string("Tara ausgefuehrt", 4)
        hx.tare()
        time.sleep(0.2)


    try:
        val = max(0, int(hx.get_weight(5)))
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

    #LCD Bereinigung
    lcd.lcd_clear()
    #Messwerte auf LCD schreiben 
    lcd.lcd_display_string(str(val), 1)    
    lcd.lcd_display_string(time.strftime("%d.%m.%Y %H:%M:%S"), 2)
    
