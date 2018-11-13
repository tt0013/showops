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
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.yesday = time.strftime('%Y-%m-%d',time.localtime(time.time()- 24*60*60))
        self.userName = 'sinashow'
        self.apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'
        self.method = 'POST'
        self.accept = 'application/json'
        self.orghost = "115.231.93.52:3433"
        self.orguser = "phonecast_maintain"
        self.orgpasswd = "sBJ7_53H_x2f8uPk"
        self.orgdb = "phonecast_userstat"
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
        httpGetParams = {
            "datefrom": "%sT20:00:00+08:00" % self.yesday,
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

        upwidth,downwidth = [],[]
        for u in json.loads(up):
            upwidth.append(float(u['bandwidth']))
        for d in json.loads(down):
            downwidth.append(float(d['bandwidth']))

        data = {"upwidth": max(upwidth), "downwidth": max(downwidth)}
        return data

    def Popuwidth(self, fromday, today):
        httpHost = "https://open.chinanetcenter.com"
        httpUri = "/api/report/domainbandwidth"
        httpGetParams = {
            "datefrom": "%s+08:00" % fromday,
            "dateto": "%s+08:00" % today,
            "type": "fiveminutes"
        }
        httpBodyParamsUP = r'''<?xml version="1.0" encoding="utf-8"?>
                                    <domain-list>
                                    <domain-name>pushws.sinashow.com</domain-name>
                                    </domain-list>'''

        httpBodyParamsDOWN = r'''<?xml version="1.0" encoding="utf-8"?>
                                    <domain-list>
                                    <domain-name>hdlnew.sinashow.com</domain-name>
                                    <domain-name>hlsws.sinashow.com</domain-name>
                                    <domain-name>pullws.sinashow.com</domain-name>
                                    <domain-name>hdlws.sinashow.com</domain-name>
                                    </domain-list>'''

        openApiDemo = AnalysisData()
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
            upwidth.append(int(float(u['bandwidth'])))
        for d in downdata:
            downtime.append(d['timestamp'])
            downwidth.append(int(float(d['bandwidth'])))

        data = {"uptime": uptime, "upwidth": upwidth,"downtime": downtime,"downwidth": downwidth}
        return data

    def SeletMysql(self, sql):
        data = []
        try:
            conn = pymssql.connect(self.orghost, self.orguser, self.orgpasswd, self.orgdb)
            cur = conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            conn.close()
        except Exception as e:
            print("Mysql Error %s" % e)
        return data

    def InsertMysql(self, sql):
        data = []
        try:
            conn = pymysql.connect(host=self.prehost, port=self.preport, user=self.preuser, passwd=self.prepasswd)
            cur = conn.cursor()
            conn.select_db(self.predb)

            cur.execute("set names utf8")
            cur.execute(sql)
            data = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("Mysql Error %s" % e)
        return data

    def GetData_Mssql(self):
        Anchor_sql = "SELECT top 1 stat_dt,anchor from t_real_num_stat with(nolock) where stat_dt>= dateadd(HH,10,'{0}') AND stat_dt< DATEADD(HH,10,'{1}') order by anchor desc".format(self.yesday, self.today)
        Users_sql = "SELECT top 1 stat_dt,crsusers from t_real_num_stat with(nolock) where stat_dt>= dateadd(HH,10,'{0}') AND stat_dt< DATEADD(HH,10,'{1}') order by crsusers desc".format(self.yesday, self.today)
        Anchor_data = self.SeletMysql(Anchor_sql)
        Users_data = self.SeletMysql(Users_sql)

        return (Anchor_data[0][1], Users_data[0][1])

    def InsertData(self,wsnum):
        SQL_Data = self.GetData_Mssql()

        Time = time.mktime(time.strptime(self.yesday, "%Y-%m-%d"))
        week = int(time.strftime("%w", time.localtime(Time)))
        anchornum = SQL_Data[0]
        useridnum = SQL_Data[1]

        '''网宿流量获取'''
        width = self.Flowcount()
        upwidth = width['upwidth']
        downwidth = width['downwidth']
        print(upwidth,downwidth)

        '''向分析数据库插入数据的sql'''
        insert_sql = '''INSERT INTO flow_fengbo_bandwidth (`DTime`,`Week`,`Usernum`,`Anchornum`,`Wangsunum`,`Upbindwidth`,`Downbindwidth`) VALUES ({0},'{1}',{2},{3},{4},{5},{6})'''.format(
            Time, self.Week[week], useridnum, anchornum, wsnum, upwidth, downwidth)
        self.InsertMysql(insert_sql)


# if __name__ == '__main__':
#     data = AnalysisData()
#     data.InsertData()





