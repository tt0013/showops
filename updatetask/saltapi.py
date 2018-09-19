#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import requests
import json,sys
import urllib3

try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 使用urllib2请求https出错，做的设置
import ssl
context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

salt_api = "https://192.168.9.126:8000/"


class SaltApi:
    """
    定义salt api接口的类
    初始化获得token
    """
    def __init__(self, url):
        self.url = url
        self.username = "saltapi"
        self.password = "yangtianqi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
            # "Content-type": "application/x-yaml"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        #self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.login_url = salt_api + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        # response = request.text
        # response = eval(response)     使用x-yaml格式时使用这个命令把回应的内容转换成字典
        response = request.json()
        return response['return'][0]

    def salt_command(self, tgt, method, arg=None, group=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        if group is not None and arg is not None:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form':group}
        elif arg is not None and group is None:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'expr_form':group}
        #print '命令参数: ', params
        result = self.get_data(self.url, params)
        return result

def refresh(salt_client):
    salt = SaltApi(salt_api)
    salt_fresh = 'saltutil.refresh_pillar'
    salt_group = 'nodegroup'
    result = salt.salt_command(salt_client, salt_fresh, None, salt_group)

    for i in result.keys():
        print(i, ': ', result[i])
    # 下面只是为了打印结果好看点
#    result2 = salt.salt_command(salt_clients, salt_method, salt_params, salt_group)
#    for i in result2.keys():
#        print i
#        print result2[i][salt_params]

def client(salt_client,salt_params):
    salt = SaltApi(salt_api)
    salt_method = 'cmd.run'
    result = salt.salt_command(salt_client, salt_method, salt_params)

    for i in result.keys():
        print(i, ': ', result[i])

def clients(salt_client,salt_method,salt_params):
    salt = SaltApi(salt_api)
    salt_group = 'nodegroup'
    result = salt.salt_command(salt_client, salt_method, salt_params, salt_group)

    for i in result.keys():
        print(i, ': ', result[i])


if __name__ == '__main__':
    client('192.168.9.126','free -m')