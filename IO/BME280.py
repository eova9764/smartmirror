#!/usr/bin/env python
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from time import sleep

def BME_Init():
    # Initialise the BME280
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    sleep(2)
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    return bme280