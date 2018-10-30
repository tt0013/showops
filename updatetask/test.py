#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


import time
import pymysql



class AnalysisData(object):
    def __init__(self):
        self.host = "192.168.9.201"
        self.port = 3306
        self.user = "root"
        self.passwd = "sinashow"
        self.db = "network"
    '''从zabbix数据库查询相关数据'''

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
        starttime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time() - 24 * 60 * 60 * 7)), "%Y%m%d")))
        SQL_Data = self.SeleMysql("select useridnum,anchornum from network.FengBo_MaxUserTraffic where Time>= %d" % starttime)

        hostpopul = []
        userpopul = []
        for i in SQL_Data:
            hostpopul.append(i[0])
            userpopul.append(i[1])
        data = {"hostpopul":hostpopul,"userpopul":userpopul}
        return data



if __name__ == '__main__':
    # starttime = int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(time.time()- 24*60*60*7)), "%Y%m%d")))
    data = AnalysisData()
    data.AnalyData()
    # data.SeleMysql("select useridnum,anchornum from network.FengBo_MaxUserTraffic where Time>= %d" % starttime)





