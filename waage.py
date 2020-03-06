#!/usr/bin/env python3
import time

import gpiozero
import lcddriver
import RPi.GPIO as GPIO
import sys
import paho.mqtt.client as mqtt
import os
from gpiozero import DigitalOutputDevice

################################################################

name = "kein name"
def on_message(client, userdata, message):
    global name
    name = str(message.payload.decode("utf-8"))
topics = ["name"]
client = mqtt.Client()
client.on_message=on_message
client.connect("127.0.0.1", 1883, 180)
client.loop_start()
for name in topics:
        client.subscribe("name/reader")
        client.loop_start()

client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)
client.loop_start()

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


mymux = HP4067Mux(22, 27, 23, 24)


####################################################################




GPIO.setmode(GPIO.BCM) 

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) 





################################################################

EMULATE_HX711 = False

if EMULATE_HX711:
    from emulated_hx711 import HX711
else:
    from hx711 import HX711


def main():
    try:
        mymux.channel(15)
        #lcd = lcddriver.lcd()
        weight_sensor = HX711(17, 18)
        weight_sensor.set_reading_format("MSB", "MSB")
        weight_sensor.set_reference_unit(339)
        weight_sensor.reset()
        weight_sensor.tare()
        print("Tare done! Add weight now...")
        while True:

            input_state = GPIO.input(26)
            if input_state == False:
                lcd.lcd_display_string("Tara ausgefuehrt", 4)
                weight_sensor.tare()
                time.sleep(0.2)
              
            input_state = GPIO.input(20)
            if input_state == False:
               print("gedrueckt")
               lcd.lcd_display_string("Reboot ausgeloest", 4)
               time.sleep(3.3)
               lcd.lcd_clear()
               os.system("reboot")
               sys.exit()
            time.sleep(0.3)
            weight = max(0, int(weight_sensor.get_weight(5)))
            client.publish("huhn/waage1", weight)
            print(weight)
            weight_sensor.power_down()
            weight_sensor.power_up()
            time.sleep(0.1)
            #lcd.lcd_clear()
            #lcd.lcd_display_string(str(weight), 1)
            ##lcd.lcd_display_string(time.strftime("%d.%m.%Y %H:%M:%S"), 2)
            #lcd.lcd_display_string(str(name), 3)

    except KeyboardInterrupt:
        pass  # User can end this with Ctrl+C.
    finally:
        print("Cleaning...")
        if not EMULATE_HX711:
            GPIO.cleanup()
        print("Bye!")


if __name__ == "__main__":
    main()
