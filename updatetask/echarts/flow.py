#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import json
import time,datetime
from urllib import parse
from updatetask.echarts.openapi import OpenApiDemo


def Flowcount(link):
    today = datetime.date.today()
    yesday = today - datetime.timedelta(days=1)
    # tm = time.strftime("%H:%M:%S")
    tm = (datetime.datetime.now() - datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
    httpHost = "https://open.chinanetcenter.com"
    httpUri = "/api/report/domainbandwidth"
    httpGetParams = {
        "datefrom": "%sT%s+08:00" % (yesday,tm),
        "dateto": "%sT%s+08:00" % (today,tm),
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
    date = openApiDemo.getDate()  # 获取系统时间
    authStr = openApiDemo.getAuth(date)  # 获取鉴权参数
    headers = openApiDemo.createHeader(authStr, date)  # 获取鉴权参数
    httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
    if link == 'Up':
        link = openApiDemo.sendRequest(httpUrl, httpBodyParamsUP, headers)
    else:
        link = openApiDemo.sendRequest(httpUrl, httpBodyParamsDOWN, headers)

    timestamp = []
    bandwidth = []
    dt = json.loads(link)
    for f in dt:
        timestamp.append(f['timestamp'])
        bandwidth.append(float(f['bandwidth']))
    data = {"dates": timestamp, "flow": bandwidth}

    return data

