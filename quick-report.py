#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import requests

API_ENDPOINT = "http://helms.shelms.io/api/"

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

def main():
    # this will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    r = requests.post(API_ENDPOINT,
        data={'celsius': data.temperature})
    print(r.text)

    #r = requests.post(API_ENDPOINT +'humi/',
    #    data={'rh': data.humidity})
    #r = requests.post(API_ENDPOINT +'baro/',
    #    data={'barom': data.pressure})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

