#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


from celery import shared_task
import requests,json


@shared_task
def Smail(platform,program,group,dates):
    user_info = {
        'platform': platform,
        'program': program,
        'group': group,
        'day': dates,
        'user': 'sa1t',
        'pwd': 'saltstack'
    }
    headers = {'content-type': 'application/json'}
    r = requests.post("http://192.168.9.126:5000/mail", data=json.dumps(user_info), headers=headers)
    return r.json()

@shared_task
def Operation(platform,program,group,wk,version,ftpadd):
    user_info = {
        'platform': platform,
        'program': program,
        'group': group,
        'week': wk,
        'version': version,
        'ftpadd': ftpadd,
        'user': 'sa1t',
        'pwd': 'saltstack'
    }
    headers = {'content-type': 'application/json'}
    r = requests.post("http://192.168.9.126:5000/update", data=json.dumps(user_info), headers=headers)
    return r.json()

@shared_task
def Rlog(net,program,hostname,ip,dates):
    user_info = {
        'program': program,
        'hostname': hostname,
        'ip': ip,
        'dates': dates,
        'user': 'sa1t',
        'pwd': 'saltstack'
    }
    headers = {'content-type': 'application/json'}
    if net == 'tel':
        r = requests.post("http://122.226.254.248:5000/log", data=json.dumps(user_info), headers=headers)
    else:
        r = requests.post("http://115.231.235.153:5000/log", data=json.dumps(user_info), headers=headers)
    return r.json()


# if __name__ == '__main__':
#     upmail('SinaShow','AvsServer','SinashowAvsgroup1','2018-09-22')
#     update('SinaShow','SinashowAvsgroup1','AvsServer','Wednesday','1.1.1.1','ftp://liuyang:0wN2hFdV@ftp.intra.sinashow.com/AVS/AvsServer1.3.9.12.tar.gz')