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
# user_info = {
#     'platform':'FengBo',
#     'program':'PhoneChatServer',
#     'group':'FengBo_PhoneChat',
#     'week':'Monday',
#     'version':'0.0.93',
#     'ftpadd':'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/PhoneCRS/room_0.0.93.tar.gz',
#     'user': 'sa1t',
#     'pwd' : 'saltstack'
# }
user_info = {
    'platform':'SinaShow',
    'program':'ChatServer',
    'group':'FinanceCrs',
    'week':'Thursday',
    'version':'4.1.93',
    'ftpadd':'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/show_crs/ChatServer_4.3.1.36.zip',
    'user': 'sa1t',
    'pwd' : 'saltstack'
}
headers = {'content-type': 'application/json'}
r = requests.post("http://192.168.9.126:5000/json", data=json.dumps(user_info), headers=headers)
# r = requests.post("http://192.168.5.105:8002/json", data=json.dumps(user_info), headers=headers)
# print(r.headers)
print(r.json())
# import requests
# r = requests.post("http://192.168.5.105:8002/json", auth=('salt', 'saltstack'))
# print(r.text)