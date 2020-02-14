#!/usr/bin/env python3
import time

import lcddriver
import RPi.GPIO as GPIO
import sys
import paho.mqtt.client as mqtt
import os

GPIO.setmode(GPIO.BCM) 
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

EMULATE_HX711 = False

if EMULATE_HX711:
    from emulated_hx711 import HX711
else:
    from hx711 import HX711

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

def main():
    try:
        
        lcd = lcddriver.lcd()
        weight_sensor = HX711(5, 6)
        weight_sensor.set_reading_format("MSB", "MSB")
        weight_sensor.set_reference_unit(339)
        weight_sensor.reset()
        weight_sensor.tare()
        print("Tare done! Add weight now...")
        while True:

            input_state = GPIO.input(25)
            if input_state == False:
                lcd.lcd_display_string("Tara ausgefuehrt", 4)
                weight_sensor.tare()
                time.sleep(0.2)
              
            input_state = GPIO.input(8)
            if input_state == False:
               print("gedrueckt")
               lcd.lcd_display_string("Reboot ausgeloest", 4)
               time.sleep(3.3)
               lcd.lcd_clear()
               os.system("reboot")
               sys.exit()
            time.sleep(0.3)
            
            weight = max(0, int(weight_sensor.get_weight(5)))
            client.publish("huhn/waage", weight)
            #print(weight)
            weight_sensor.power_down()
            weight_sensor.power_up()
            time.sleep(0.1)
            lcd.lcd_clear()
            lcd.lcd_display_string(str(weight), 1)
            lcd.lcd_display_string(time.strftime("%d.%m.%Y %H:%M:%S"), 2)

    except KeyboardInterrupt:
        pass  # User can end this with Ctrl+C.
    finally:
        print("Cleaning...")
        if not EMULATE_HX711:
            GPIO.cleanup()
        print("Bye!")


if __name__ == "__main__":
    main()
