#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import datetime
from hashlib import sha256
from urllib import parse
import hmac
import base64
import requests


class OpenApiDemo:
    def getDate(self):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        date_gmt = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        return date_gmt

    def getAuth(self, userName, apikey, date):
        signed_apikey = hmac.new(apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
        signed_apikey = base64.b64encode(signed_apikey)
        signed_apikey = userName + ":" + signed_apikey.decode()
        signed_apikey = base64.b64encode(signed_apikey.encode('utf-8'))
        return signed_apikey

    def createHeader(self, userName, accept, authStr, date):
        headers = {
            'Date': date,
            'Accept': accept,
            'Content-type': accept,
            'Authorization': 'Basic ' + authStr.decode()
        }
        return headers

    def sendRequest(self, httpUrl, method, httpGetParams, httpBodyParams, headers):
        if method.upper() == 'POST':
            resp = requests.post(httpUrl, data=httpBodyParamsJSON, headers=headers)
        elif method.upper() == 'GET':
            resp = requests.get(httpUrl, params=httpBodyParamsJSON, headers=headers)
        self.printResp(resp)

    def printResp(self, resp):
        headers_post = dict(resp.headers);
        str = "{}\nServer:{}\nDate:{}\nContent-Length:{}\nConnection:{}\nx-cnc-request-id:{}\n\n{}".format(
            resp.status_code,
            headers_post['Server'],
            headers_post['Date'],
            headers_post['Content-Length'],
            headers_post['Connection'],
            headers_post['x-cnc-request-id'],
            resp.text)
        str_new_json = {'data': str, 'resultCode': 'success'}
        print(str_new_json)


if __name__ == '__main__':
    '''
        输入参数部分 begin
    '''
    userName = 'sinashow'  # 替换成真实账号
    apikey = 'qYRZvZWXdttqN6PgXMYL7uwmZQfC'  # 替换成真实账号的apikey
    method = 'POST'  # 填写请求方法post/get
    accept = 'application/json'  # 填写返回接收数据模式
    httpHost = "https://open.chinanetcenter.com"
    httpUri = "/api/report/visitor/total/stream"
    httpGetParams = {
        "datefrom": "2017-03-01T08:55:00+08:00",
        "dateto": "2017-03-01T09:14:59+08:00",
        "type": "fiveminutes"
    }
    httpBodyParamsXML = r'''<?xml version="1.0" encoding="utf-8"?>
							<domain-list>
							<domain-name>www.example1.com</domain-name>
							<domain-name>www.example2.com</domain-name>
							</domain-list>'''
    httpBodyParamsJSON = '[{"domain":"www.test.com"}]'
    '''
        输入参数部分  end
    '''

    ##
    openApiDemo = OpenApiDemo()
    date = openApiDemo.getDate()  # 获取系统时间
    authStr = openApiDemo.getAuth(userName, apikey, date)  # 获取鉴权参数
    headers = openApiDemo.createHeader(userName, accept, authStr, date)  # 获取鉴权参数
    httpUrl = httpHost + httpUri + "?" + parse.urlencode(httpGetParams)
    openApiDemo.sendRequest(httpUrl, method, httpGetParams, httpBodyParamsJSON, headers)
