#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,os,stat
import zipfile,tarfile
import shutil,json
import subprocess
# from replace import replace
from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)

parser_post = reqparse.RequestParser()
parser_post.add_argument("user", type=str, required=True)
parser_post.add_argument("pwd", type=str, required=True)
parser_post.add_argument("platform", type=str, required=True)
parser_post.add_argument("program", type=str, required=True)
parser_post.add_argument("group", type=str, required=True)
parser_post.add_argument("week", type=str, required=True)
parser_post.add_argument("version", type=str, required=True)
parser_post.add_argument("ftpadd", type=str, required=True)

class Async(object):
    def __init__(self,args):
        self.args = args
        self.pkgdir = 'pkg'
        self.Initialdir = os.getcwd()

    def tarpkg(self):
        zipf = self.args['ftpadd'].split('/').pop()
        if os.path.exists(self.Initialdir + '/' + zipf):
            os.remove(self.Initialdir + '/' + zipf)
        ftp = subprocess.call("wget %s" % self.args['ftpadd'], shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        if ftp == 0:
            if os.path.isdir(self.Initialdir + '/' + self.pkgdir):
                 shutil.rmtree(self.Initialdir + '/' + self.pkgdir)
                 os.mkdir(self.pkgdir)
            zipf = self.Initialdir + '/' + zipf
            if self.args['program'] == "PhoneChatServer" or self.args['program'] == "AvsServer":
                 tar = tarfile.open(zipf, "r")
                 for f in tar:
                    tar.extract(f,self.Initialdir + '/' + self.pkgdir)
                 tar.close()
                 newfile = tarfile.open(self.args['program'] + '-' + self.args['version'] + '.tar.gz', "w:gz")
                 os.chdir(self.pkgdir)
                 for root, dir, files in os.walk(self.Initialdir + '/' + self.pkgdir):
                     for f in files:
                         os.chmod(self.Initialdir + '/' + self.pkgdir + '/' + f, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
                         newfile.add(f)
                 newfile.close()
                 nfile = self.Initialdir + '/' + self.args['program'] + '-' + self.args['version'] + '.tar.gz'
            else:
                 pkgzip = zipfile.ZipFile(zipf, 'r')
                 for f in pkgzip.namelist():
                     pkgzip.extract(f, self.Initialdir + '/' + self.pkgdir)
                     os.chmod(self.Initialdir + '/' + self.pkgdir + '/' + f, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
                 pkgzip.close()
                 newfile = tarfile.open(self.args['program'] + '-' + self.args['version'] + '.tar.gz', "w:gz")
                 os.chdir(self.pkgdir)
                 for root, dir, files in os.walk(self.Initialdir + '/' + self.pkgdir):
                     for f in files:
                         newfile.add(f)
                 newfile.close()
                 nfile = self.Initialdir + '/' + self.args['program'] + '-' + self.args['version'] + '.tar.gz'
            try:
                if self.args['group'] == "NobusinessCrs":
                    shutil.move(nfile, '/srv/salt/Sinashow_one/files/')
                elif self.args['group'] == "FinanceCrs":
                    shutil.move(nfile, '/srv/salt/Sinashow_two/files/')
                elif self.args['group'] == "FengBo_PhoneChat":
                    shutil.move(nfile, '/srv/salt/FengBo_PhoneChat/files/')
                else:
                    shutil.move(nfile, '/srv/salt/Sinashow/files/')
                os.remove(zipf)
            except shutil.Error:
#                return False
                print('a')
        else:
           # return False
            print('b')


# def to_do(arg1, args2):
#     return str(arg1)+str(args2)

# 操作（post / get）资源列表
class TodoList(Resource):

    def post(self):
        args = parser_post.parse_args()
        # 构建新参数
        if args['user'] == "sa1t" and args['pwd'] == "saltstack":
            if args['group'] == "NobusinessCrs":
                fdir = '/srv/salt/Sinashow_one/files/'
            elif args['group'] == "FinanceCrs":
                fdir = '/srv/salt/Sinashow_two/files/'
            elif args['group'] == "FengBo_PhoneChat":
                fdir = '/srv/salt/FengBo_PhoneChat/files/'
            else:
                fdir = '/srv/salt/Sinashow/files/'
        # 调用方法to_do
            tar = Async(args)
            info = {"info": tar.tarpkg()}
        # # 资源添加成功，返回201
            return info,201
        else:
            abort(400)



# 设置路由，即路由地址为http://127.0.0.1:5000/users
api.add_resource(TodoList, "/json")

# @app.route('/json', methods=['POST'])
# def my_json():
#     print(request.headers)
#     print(request.json)
#     rt = {'info':'hello '+request.json['week']}
#     return Response(json.dumps(rt),  mimetype='application/json')


if __name__ == '__main__':
    app.run(host='192.168.5.105',port='8002',debug=True)