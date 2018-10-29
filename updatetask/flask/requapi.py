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
    'program':'AvsServer',
    'hostname':'Avs-38-gansu-tel-SHOW',
    'ip':'60.165.99.38',
    # 'program': 'ChatServer',
    # 'hostname': 'Chat-141-jihua-Double-SHOW',
    # 'ip': '122.226.254.141',
    'dtime':'2018-10-17',
    'user': 'sa1t',
    'pwd' : 'saltstack'
}
# user_info = {
#     'platform':'SinaShow',
#     'program':'AvsServer',
#     'group':'SinashowAvsgroup1',
#     'week':'Saturday',
#     'version':'1.3.9.12',
#     'ftpadd':'ftp://liuyang:0wN2hFdV@ftp.intra.sinashow.com/AVS/AvsServer1.3.9.12.tar.gz',
#     'user': 'sa1t',
#     'pwd' : 'saltstack'
# }
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
# r = requests.post("http://192.168.9.126:5000/update", data=json.dumps(user_info), headers=headers)
r = requests.post("http://122.226.254.248:5000/log", data=json.dumps(info), headers=headers)
# r = requests.post("http://192.168.5.105:8002/login", data=json.dumps(user_info), headers=headers)
# print(r.headers)
print(r.json())
# import requests
# r = requests.post("http://192.168.5.105:8002/json", auth=('salt', 'saltstack'))
# print(r.text)