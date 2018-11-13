#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


import time
import pymysql
import hmac
import json
import base64
import requests
import datetime
from urllib import parse
from hashlib import sha256



class AnalysisData(object):
    def __init__(self):
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.yesday = time.strftime('%Y-%m-%d',time.localtime(time.time()- 24*60*60))
        self.userName = 'sinashow'
        self.apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'
        self.method = 'POST'
        self.accept = 'application/json'
        self.orghost = "192.168.9.126"
        self.orgport = 3306
        self.orguser = "root"
        self.orgpasswd = "sinashow"
        self.orgdb = "TrafficStatis"
        self.prehost = "192.168.9.126"
        self.preport = 3306
        self.preuser = "root"
        self.prepasswd = "sinashow"
        self.predb = "CMDB"
        self.Week = {0:'日',1:'一',2:'二',3:'三',4:'四',5:'五',6:'六'}

    def getDate(self):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        date_gmt = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        return date_gmt

    def getAuth(self, date):
        signed_apikey = hmac.new(self.apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
        signed_apikey = base64.b64encode(signed_apikey)
        signed_apikey = self.userName + ":" + signed_apikey.decode()
        signed_apikey = base64.b64encode(signed_apikey.encode('utf-8'))
        return signed_apikey

    def createHeader(self, authStr, date):
        headers = {
            'Date': date,
            'Accept': self.accept,
            'Content-type': self.accept,
            'Authorization': 'Basic ' + authStr.decode()
        }
        return headers

    def sendRequest(self, httpUrl, httpBodyParams, headers):
        if self.method.upper() == 'POST':
            resp = requests.post(httpUrl, data=httpBodyParams, headers=headers)
        elif self.method.upper() == 'GET':
            resp = requests.get(httpUrl, params=httpBodyParams, headers=headers)

        return resp.text

    def Flowcount(self):
        httpHost = "https://open.chinanetcenter.com"
        httpUri = "/api/report/domainbandwidth"
        # httpGetParams = {
        #     "datefrom": "%sT10:00:00+08:00" % self.yesday,
        #     "dateto": "%sT02:00:00+08:00" % self.today,
        #     "type": "fiveminutes"
        # }

        httpBodyParamsUP = r'''<?xml version="1.0" encoding="utf-8"?>
                                    <domain-list>
                                    <domain-name>pushws.sinashow.com</domain-name>
                                    </domain-list>'''

        httpBodyParamsDOWN = r'''<?xml version="1.0" encoding="utf-8"?>
                                    <domain-list>
                                    <domain-name>hdlnew.sinashow.com</domain-name>
                                    <domain-name>hdlws.sinashow.com</domain-name>
                                    <domain-name>hlsws.sinashow.com</domain-name>
                                    <domain-name>pullws.sinashow.com</domain-name>
                                    </domain-list>'''

        openApiDemo = AnalysisData()
        date = self.getDate()  # 获取系统时间
        authStr = self.getAuth(date)  # 获取鉴权参数
        headers = self.createHeader(authStr, date)  # 获取鉴权参数
        Week = {0: '日', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六'}
        for i in range(7):
            Today = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60 * i))
            before_day = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60 * (i + 1)))
            Time = time.mktime(time.strptime(before_day, "%Y-%m-%d"))
            week = int(time.strftime("%w", time.localtime(Time)))
            httpGetParams = {
                "datefrom": "%sT10:00:00+08:00" % before_day,
                "dateto": "%sT02:00:00+08:00" % Today,
                "type": "fiveminutes"
            }
            httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
            up = openApiDemo.sendRequest(httpUrl, httpBodyParamsUP, headers)
            down = openApiDemo.sendRequest(httpUrl, httpBodyParamsDOWN, headers)

            upwidth,downwidth = [],[]
            for u in json.loads(up):
                upwidth.append(float(u['flow']))
            for d in json.loads(down):
                downwidth.append(float(d['flow']))

            print(Time, Week[week],max(upwidth),max(downwidth))

if __name__ == '__main__':
    d = AnalysisData()
    print(d.Flowcount())



