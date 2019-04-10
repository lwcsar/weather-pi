#!/usr/bin/env python3
import os
import requests
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106


from PIL import ImageFont

import smbus2
import bme280

def do_nothing(obj):
    pass

def date_time():
    f = os.popen('date +"%a %x %H:%M:%S"')
    dt = str(f.read())
    return "%s" % dt.rstrip('\r\n').rstrip(' ')

def lan_ip():
    cmd = 'hostname -I'
    f = os.popen(cmd)
    ip = str(f.read())
    return "IP: %s" % ip.rstrip('\r\n').rstrip(' ')

def temperature():
    # this will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)
    return "%0.0f\u00b0F" % ((data.temperature * 9/5)+32)

# define our i2c LED location
serial = i2c(port=1, address=0x3C)
# We have an ssd1306 device so we initialize it at the 
# serial address we created.
device = ssd1306(serial)
# This line keeps the display from immediately turning off once the
# script is complete.
device.cleanup = do_nothing

# Setup our Temperature sensor (bme280)
port = 4
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

freemono = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 32)

with canvas(device) as draw:
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.rectangle([(2,10),(127,50)], outline="white", fill="black")
    draw.text((10, 10), "%3.2f C" % (data.temperature), font=freemono, fill="white")
    draw.text((20, 10), str(data.temperature*9/5+32), font=freemono, fill="white")
    draw.text((20, 10), "%3.2f F" % (data.temperature*9/5+32),font=freemono,fill="white")
    draw.text((30, 10), temperature(), font=freemono, fill="white")

print("%3.2f" % data.temperature)
print("%3.2f" % (data.temperature*9/5+32) )
