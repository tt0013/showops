#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import requests, json
github_url = "http://192.168.5.105:8002/add_task/"
data = json.dumps({'platform':'test'})
print(data)
r = requests.post(github_url, data)
print(r.json)