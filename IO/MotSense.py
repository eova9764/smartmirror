#!/usr/bin/env python
from time import sleep
import RPi.GPIO as gpio
import subprocess

sensePin = 4

gpio.setmode(gpio.BCM)
gpio.setup(sensePin, gpio.IN)

def get():
    return 1-gpio.input(sensePin)

if __name__ == '__main__':
    while True:
        sleep(0.1)
        print(gpio.input(sensePin)==0)
