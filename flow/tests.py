#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import time
import pymysql
import pymssql
import hmac
import json
import base64
import requests
import datetime
from urllib import parse
from hashlib import sha256

class AnalysisData(object):
    def __init__(self):
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24*60*60*0))
        self.yesday = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24*60*60*1))
        self.ntime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.userName = 'sinashow'
        self.apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'
        self.method = 'POST'
        self.accept = 'application/json'
        self.orghost = "115.231.93.52:3433"
        self.orguser = "phonecast_maintain"
        self.orgpasswd = "sBJ7_53H_x2f8uPk"
        self.orgdb = "phonecast_userstat"
        self.prehost = "192.168.9.18"
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
        httpGetParams = {
            "datefrom": "%sT00:10:00+08:00" % self.yesday,
            "dateto": "%sT00:10:00+08:00" % self.today,
            "type": "fiveminutes"
        }

        httpBodyParams = r'''<?xml version="1.0" encoding="utf-8"?>
                                    <domain-list>
                                    <domain-name>hdlnew.sinashow.com</domain-name>
                                    <domain-name>hdlws.sinashow.com</domain-name>
                                    <domain-name>hlsws.sinashow.com</domain-name>
                                    <domain-name>pullws.sinashow.com</domain-name>
                                    </domain-list>'''

        openApiDemo = AnalysisData()
        date = self.getDate()
        authStr = self.getAuth(date)
        headers = self.createHeader(authStr, date)
        httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
        width = openApiDemo.sendRequest(httpUrl, httpBodyParams, headers)

        countwidth = []
        for w in json.loads(width):
            countwidth.append(round(float(w['bandwidth'])))
        data = {"countwidth": max(countwidth)}
        return data


    def Maxtime(self):
        httpHost = "https://open.chinanetcenter.com"
        httpUri = "/api/report/domainbandwidth"
        httpGetParams = {
            "datefrom": "%sT00:20:00+08:00" % self.yesday,
            "dateto": "%sT02:00:00+08:00" % self.today,
            "type": "fiveminutes"
        }
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
        httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
        up = openApiDemo.sendRequest(httpUrl, httpBodyParamsUP, headers)
        down = openApiDemo.sendRequest(httpUrl, httpBodyParamsDOWN, headers)

        countwidth = []
        for w in json.loads(up):
            countwidth.append(float(w['bandwidth']))
        uptime = max(countwidth)
        for w in json.loads(up):
            if uptime == float(w['bandwidth']):
                uptime = w['timestamp']
        for w in json.loads(down):
            countwidth.append(float(w['bandwidth']))
        dtime = max(countwidth)
        for w in json.loads(down):
            if dtime == float(w['bandwidth']):
                dtime = w['timestamp']
        upend = datetime.datetime.strptime(uptime, "%Y-%m-%d %H:%M:%S")
        upstart = (upend-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        dend = datetime.datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
        dstart = (dend-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        print(upstart,upend,dstart,dend)
        data = {"uptime": uptime, "dtime": dtime}
        return data

if __name__ == '__main__':
    data = AnalysisData()
    # print(data.Flowcount())
    print(data.Maxtime())
