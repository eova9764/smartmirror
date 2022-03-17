#!/usr/bin/env python
from time import sleep
import RPi.GPIO as gpio
import subprocess

sensePin = 4

ds = 0
timeout = 10
timer = timeout
once = False
once2 = False

gpio.setmode(gpio.BCM)
gpio.setup(sensePin, gpio.IN)

def get():
    return 1-gpio.input(sensePin)

if __name__ == '__main__':
    while True:
        sleep(1)
        ds = 0
        motion = 1-gpio.input(sensePin)
        if motion == 1:
            once2 = False
            timer = 0
            if once == False:
                once = True
                print("Wake")
        else:
            if timer >= timeout:
                if once2 == False:
                    once2 = True
                    once = False
                    print("Sleep")
            else:
                timer = timer + 1
