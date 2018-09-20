#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import requests,json
#
# user_info = {'name': 'letian', 'password': '123'}
# r = requests.post("http://192.168.5.105:8002/register", data=user_info)
#
# print(r.text)

# import requests, json
#
user_info = {
    'platform':'SinaShow',
    'program':'ChatServer',
    'group':'FinanceCrs',
    'day':'2018-09-20',
    'version':'0.0.93',
    'user': 'sa1t',
    'pwd' : 'saltstack'
}
# user_info = {
#     'platform':'SinaShow',
#     'program':'ChatServer',
#     'group':'FinanceCrs',
#     # 'week':'Monday',
#     'week':'Tuesday',
#     'version':'4.1.9.15',
#     'ftpadd':'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/show_crs/ChatServer_4.3.1.36.zip',
#     'user': 'sa1t',
#     'pwd' : 'saltstack'
# }
headers = {'content-type': 'application/json'}
r = requests.post("http://192.168.9.126:5000/mail", data=json.dumps(user_info), headers=headers)
# r = requests.post("http://192.168.5.105:8002/json", data=json.dumps(user_info), headers=headers)
# print(r.headers)
print(r.json())
print(type(r.json()))
# import requests
# r = requests.post("http://192.168.5.105:8002/json", auth=('salt', 'saltstack'))
# print(r.text)