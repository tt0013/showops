#!/usr/bin/env python
# -*-coding:utf-8-*-

import urllib
import urllib.parse
import urllib.request
# import urllib2　　　　#python2.x需要引入
import ssl, json

context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_stdlib_context

class SaltAPI(object):
    __token_id = ''

    def __init__(self, url, username, password):
        self.__url = url.strip()
        self.__user = username
        self.__password = password

    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode_params = urllib.parse.urlencode(params).encode(encoding='utf-8')
        content = self.postRequest(encode_params,prefix = '/login')
        self.__token_id = content['return'][0]['token']
        # print(self.__token_id)


    def postRequest(self, params, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, params, headers=headers)
        data = urllib.request.urlopen(req).read().decode("utf-8")
        content = json.loads(data)
        return content

    def salt_alive(self, tgt):
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        obj = urllib.parse.urlencode(params).encode(encoding='utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        print(ret)
        return ret

if __name__ == '__main__':
    v = SaltAPI("https://183.131.205.49:8000", username="saltapi", password="yangtianqi")
    v.salt_alive('122.226.254.211')