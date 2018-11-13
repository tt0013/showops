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
        self.userName = 'sinashow'
        self.apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'
        self.method = 'POST'
        self.accept = 'application/json'
        self.host = "192.168.9.126"
        self.port = 3306
        self.user = "root"
        self.passwd = "sinashow"
        self.db = "CMDB"
        self.today = datetime.date.today()
        self.yesday = self.today - datetime.timedelta(days=1)

    def SeleMysql(self, sql):
        data = []
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
            cur = conn.cursor()
            conn.select_db(self.db)

            cur.execute("set names utf8")
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            print("Mysql Error %s" % e)
        return data
    def AnalyData(self):
        Selectsql = "select Dates from flow_fengbo_bandwidth where id>%d" % 6
        SQL_Data = self.SeleMysql(Selectsql)
        return SQL_Data



if __name__ == '__main__':
    data = AnalysisData()
    print(data.AnalyData())





