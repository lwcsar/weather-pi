#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Portions copyright (c) 2014-18 Richard Hull and contributors
# PYTHON_ARGCOMPLETE_OK
import os
import sys
import time
import requests

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

API_ENDPOINT = "http://weather.shelms.io/api/"

if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

from PIL import ImageFont

try:
    from luma.core.virtual import terminal
    from luma.core.render import canvas
    pass
except ImportError:
    print("Luma.core not installed. Run:")
    print("git clone https://github.com/rm-hull/luma.core.git")
    sys.exit()

try:
    import smbus2
    import bme280
except ImportError:
    print("The smbus2 or bme280 libraries were not found. Run 'sudo -H pip install RPi.bme280' to install it.")
    sys.exit()

port = 4
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def do_nothing():
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


def temperature(type='temp'):
    # this will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)
    if type == 'humidity':
    	return "%0.2f%% rH" % \
           (data.humidity)
    elif type == 'pressure':
    	return "%0.2f hPa" % \
           (data.pressure)
    elif type == 'tempf':
    	return "%0.0f\u00b0F" % \
           ((data.temperature * 9/5)+32)
    elif type == 'tempc':
    	return "%0.2f\u00b0C" % \
           (data.temperature)
    else:
    	return "%0.2fC, %0.2fF" % \
           (data.temperature, (data.temperature * 9/5)+32)

def stats(device):
    font_sm = ImageFont.truetype("Piboto-Regular.ttf", 11)
    font_lg = ImageFont.truetype("Piboto-Regular.ttf", 18)
    font_xl = ImageFont.truetype("Piboto-Regular.ttf", 40)
    font_d = ImageFont.load_default().font

    with canvas(device) as draw:
        draw.text((0, 0), date_time(), font=font_sm, fill="white")
        draw.text((0, 52), lan_ip(), font=font_sm, fill="white")
        draw.text((20, 6), temperature('tempf'), font=font_xl, fill="white")

def report():
    # this will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    r = requests.post(API_ENDPOINT +'temp/',
        data={'celsius': data.temperature})
    print(r.text)

    r = requests.post(API_ENDPOINT +'humi/',
        data={'rh': data.humidity})

    r = requests.post(API_ENDPOINT +'baro/',
        data={'barom': data.pressure})


def main():
    time_counter = 0

    # define our i2c LED location
    serial = i2c(port=1, address=0x3C)

    # We have an ssd1306 device so we initialize it at the 
    # serial address we created.
    oled_device = ssd1306(serial)

    # This line keeps the display from immediately turning off once the
    # script is complete.
    oled_device.cleanup = do_nothing

    while True:
        stats(oled_device)
        time.sleep(5)
        if (time_counter % 300 == 0):
            report()
        time_counter += 5


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

