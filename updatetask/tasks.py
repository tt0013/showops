#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


from celery import shared_task
import requests,json
from itom.models import Renewmail

@shared_task
def upmail(platform,program,group,dates):
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

# if __name__ == '__main__':
#     upmail('SinaShow','AvsServer','SinashowAvsgroup1','2018-09-22')