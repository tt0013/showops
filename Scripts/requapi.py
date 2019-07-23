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
info = {
    'user': 'root',
    'pwd': 'ldapsudo'
}
user_info = {
    'platform':'SinaShow',
    'program':'ChatServer',
    'group':'BusinessCrs',
    'week':'Saturday',
    'version':'4.3.1.36',
    'ftpadd':'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/show_crs/ChatServer_4.3.1.36.zip',
    'user': 'sa1t',
    'pwd' : 'saltstack',
    'ms5' : '1,2'
}
# user_info = {
#     'platform': 'FengBo',
#     'program': 'PhoneChatServer',
#     'group': 'FengBo_PhoneChat',
#     'week': 'Saturday',
#     'version': '0.0.96',
#     'ftpadd':'ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/PhoneCRS/room.tar.gz',
#     'user': 'sa1t',
#     'pwd' : 'saltstack'
# }
headers = {'content-type': 'application/json'}
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
# r = requests.post("http://192.168.9.126:5000/mail", data=json.dumps(user_info), headers=headers)
r = requests.post("http://192.168.9.126:5000/update", data=json.dumps(user_info), headers=headers)
# r = requests.post("http://122.226.254.248:5000/log", data=json.dumps(info), headers=headers)
# r = requests.post("http://192.168.9.18:3800/sudoauth", data=json.dumps(info), headers=headers)
# print(r.headers)
print(r.json())
# print(json.loads(r.json()))
# import requests
# r = requests.post("http://192.168.5.105:8002/json", auth=('salt', 'saltstack'))
# print(r.text)