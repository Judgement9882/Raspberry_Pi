#!/usr/bin/python

import spidev
import time
import os

spi = spidev.SpiDev()
spi.open(0,0) # CE0 bus / CH0 device
spi.max_speed_hz = 500000

def ReadChannel(channel):
    adc = spi.xfer2([ 6|(channel&4) >> 2, (channel&3) << 6, 0])
    data = ((adc[1] & 0x0f) << 8) + adc[2] # 12bits data
    return data

def ConvertVolts(data):
    volts = (data * 3.3) / float(4095) # calculate voltage value
    volts = round(volts, 2) # round at 2
    return volts

channel = 0 # CH0
delay = 2 # delay 2s

while True:
    level = ReadChannel(channel)
    volts = ConvertVolts(level)
    print("-----------------")
    print("Value : {} ({}v)".format(level, volts))
    time.sleep(delay)
