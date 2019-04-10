#!/usr/bin/env python3

import requests

API_URL = 'http://helms.shelms.io/api'

data = {'celsius': 32.1}
r = requests.post(API_URL, data)
print(r.text)

r = requests.get('http://helms.shelms.io/api/')
print(r.text)
