#!/usr/bin/env python

import bme280
import time
import smbus
import sys
from beebotte import *

# Set up the I2C bus for the TSL2561 sensor
bus = smbus.SMBus(1)

# Replace CHANNEL_TOKEN with that of your Beebotte channel and YOUR_CHANNEL_NAME with the name you give your Beebotte channel
bbt = BBT(token = 'CHANNEL_TOKEN')
chanName = "YOUR_CHANNEL_NAME"

# Set the time to wait between sending data to Beebotte. Avoid lower values due to API limitations. Default is 900 seconds (15 mins).
period = 900

# These resources needed to be added to your Beebotte channel - make sure the channel resource names match!
temperature_resource   = Resource(bbt, chanName, 'temperature')
humidity_resource = Resource(bbt, chanName, 'humidity')
pressure_resource = Resource(bbt, chanName, 'pressure')
luminosity_resource = Resource(bbt, chanName, 'luminosity')

# Read the luminosity data from the TSl2561 sensor
def get_luminosity():
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
    bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
    time.sleep(0.5)
    full_data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    ir_data = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    full_spectrum = full_data[1] * 256 + full_data[0]
    infrared = ir_data[1] * 256 + ir_data[0]
    visible = full_spectrum - infrared
    return visible

# The main part. Get the data from the sensors, then sent it to your Beebotte channel.
def run():
  while True:
    temperature, pressure, humidity = bme280.readBME280All()
    luminosity = get_luminosity()
    if temperature is not None and humidity is not None and pressure is not None and luminosity is not None:
        try:
          temperature_resource.write(temperature)
          humidity_resource.write(humidity)
          pressure_resource.write(pressure)
          luminosity_resource.write(luminosity)
        except Exception:
          print ("Error while writing to Beebotte")
    else:
        print ("Failed to get readings. Try again!")

    time.sleep(period)

run()