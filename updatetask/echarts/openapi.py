#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import hmac
import json
import base64
import requests
import datetime
from urllib import parse
from hashlib import sha256


class OpenApiDemo(object):
    def __init__(self):
        self.userName = 'sinashow'
        self.apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'
        self.method = 'POST'
        self.accept = 'application/json'


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
        today = datetime.date.today()
        yesday = today - datetime.timedelta(days=1)
        # tm = time.strftime("%H:%M:%S")
        tm = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
        httpHost = "https://open.chinanetcenter.com"
        httpUri = "/api/report/domainbandwidth"
        httpGetParams = {
            "datefrom": "%sT%s+08:00" % (yesday, tm),
            "dateto": "%sT%s+08:00" % (today, tm),
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

        openApiDemo = OpenApiDemo()
        date = self.getDate()  # 获取系统时间
        authStr = self.getAuth(date)  # 获取鉴权参数
        headers = self.createHeader(authStr, date)  # 获取鉴权参数
        httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
        up = openApiDemo.sendRequest(httpUrl, httpBodyParamsUP, headers)
        down = openApiDemo.sendRequest(httpUrl, httpBodyParamsDOWN, headers)

        uptime,upwidth,downtime,downwidth = [],[],[],[]
        updata = json.loads(up)
        downdata = json.loads(down)
        for u in updata:
            uptime.append(u['timestamp'])
            upwidth.append(float(u['flow']))
        for d in downdata:
            downtime.append(d['timestamp'])
            downwidth.append(float(d['flow']))

        data = {"uptime": uptime, "upwidth": upwidth,"downtime":downtime,"downwidth":downwidth}

        return data

    def Popucount(self):
        tdict,updict,downdict = {},{},{}
        days = datetime.date.today()
        httpHost = "https://open.chinanetcenter.com"
        httpUri = "/api/report/domainbandwidth"
        for i in range(7):
            i += 1
            tdict[str(days - datetime.timedelta(days=i))] = str(days - datetime.timedelta(days=i + 1))

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

        openApiDemo = OpenApiDemo()
        date = self.getDate()  # 获取系统时间
        authStr = self.getAuth(date)  # 获取鉴权参数
        headers = self.createHeader(authStr, date)  # 获取鉴权参数
        for t,y in tdict.items():
            httpGetParams = {
                "datefrom": "%sT00:00:00+08:00" % (y),
                "dateto": "%sT00:00:00+08:00" % (t),
                "type": "fiveminutes"
            }
            httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
            updata = openApiDemo.sendRequest(httpUrl, httpBodyParamsUP, headers)
            downdata = openApiDemo.sendRequest(httpUrl, httpBodyParamsDOWN, headers)
            updict[t] = updata
            downdict[t] = downdata
        uptime, upwidth, downtime, downwidth = [], [], [], []
        for k,v in updict.items():
            if k:
                d = []
                for i in json.loads(v):
                    d.append(float(i['flow']))
                uptime.append(k)
                upwidth.append(max(d))
        for k,v in downdict.items():
            if k:
                d = []
                for i in json.loads(v):
                    d.append(float(i['flow']))
                downtime.append(k)
                downwidth.append(max(d))
        popudata = {"uptime": uptime[::-1], "upwidth": upwidth[::-1], "downtime": downtime[::-1], "downwidth": downwidth[::-1]}

        return popudata



