#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,os,stat
import zipfile,tarfile
import shutil,json
import subprocess
from replace import replace
from flask import Flask, request, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
import os,smtplib,configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from updatetask.CreateHtml import CreateHtml


app = Flask(__name__)
api = Api(app)

parser_post = reqparse.RequestParser()
parser_post.add_argument("user", type=str, required=True)
parser_post.add_argument("pwd", type=str, required=True)
parser_post.add_argument("platform", type=str, required=True)
parser_post.add_argument("program", type=str, required=True)
parser_post.add_argument("group", type=str, required=True)
parser_post.add_argument("week", type=str)
parser_post.add_argument("version", type=str)
parser_post.add_argument("ftpadd", type=str)
parser_post.add_argument("day", type=str)

class SendMail(object):
    def __init__(self,args):
        self.args = args
        self.username = 'monitor@sinashow.com'
        self.passwd = 'monitor'
        # self.recv = ['yangtianqi@sinashow.com','tt06090013@163.com']
        self.recv = ['yangtianqi@sinashow.com']
        self.filename = r'E:\PycharmScript\CMDB\showops\updatetask\CreateHtml\CreateHtml.html'
        self.email_host = 'mail.sinashow.com'
        self.port = 25


    def send_mail(self):
        try:
            CreateHtml.CreateHtml(self.filename, self.args['platform'], self.args['program'], self.args['day'])
        except Exception as e:
            return e

        msg = MIMEMultipart()
        #发送内容的对象
        if self.filename:#处理附件的
            html = open(self.filename,'r',encoding='utf-8').read()
            html_part = MIMEText(html, 'html', 'utf-8')
            msg.attach(html_part)
        # 邮件主题
        if self.args['platform'] == 'SinaShow':
            msg['Subject'] = u'[重要通知]-[程序更新]-[SHOW平台程序更新]-[%s]' % self.args['day']
        else:
            msg['Subject'] = u'[重要通知]-[程序更新]-[疯播平台程序更新]-[%s]' % self.args['day']
        msg['From'] = 'Automation Program <%s>' % self.username  # 发送者账号
        msg['To'] = ';'.join(self.recv)  # 接收者账号列表
        self.smtp = smtplib.SMTP(self.email_host,port=self.port)
        #发送邮件服务器的对象
        self.smtp.login(self.username,self.passwd)
        try:
            self.smtp.sendmail(self.username,self.recv,msg.as_string())
        #记录邮件状态，发送更新后的信息
            conf = configparser.ConfigParser()
            conf.add_section('MAIL')
            conf.set('MAIL', 'platform', self.args['platform'])
            conf.set('MAIL', 'program', self.args['program'])
            conf.set('MAIL', 'group', self.args['group'])
            conf.set('MAIL', 'date', self.args['day'])
            conf.set('MAIL', 'state', '1')
            with open(r'E:\PycharmScript\CMDB\showops\updatetask\CreateHtml\mail.ini', "w",encoding='utf-8') as f:
                conf.write(f)
            return "Success"
        except Exception:
            return "2"


    # def __del__(self):
    #     self.smtp.quit()


class Async(object):
    def __init__(self,args,fdir=None):
        self.args = args
        self.fdir = fdir
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
            if self.args['program'] == "ChatServer":
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
            else:
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
            os.chdir(self.Initialdir)
            nfile = self.Initialdir + '/' + self.args['program'] + '-' + self.args['version'] + '.tar.gz'
            os.remove(zipf)
            shutil.move(nfile, self.fdir+'files/')
            return "success"
        else:
           # return False
            return 'b'

    def excute(self):
        i = 0
        w = 0
        with open('/srv/pillar/schedule.sls', 'w') as sls:
            sls.write('schedule:\n')
            sls.write('  highstate:\n')
            sls.write('    function: state.highstate\n')
            sls.write('    when:       %s     5:00am\n' % self.args['week'])
        try:
            subprocess.check_call("/usr/bin/salt -N %s saltutil.refresh_pillar " % self.args['group'], shell=True)
#            subprocess.call("/usr/bin/salt -N %s saltutil.refresh_pillar " % self.group, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
            result = subprocess.Popen("/usr/bin/salt -N %s pillar.get schedule" % self.args['group'], shell=True,
                                      stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            return 1
        for line in result.stdout.readlines():
            line = line.strip('\n')
            ip = re.search(r'(\d+\.){3}\d+', line)
            wk = re.search(r'^\s+%s\s+%s' % (self.args['week'],'5:00am'), line)
            if ip:
                i += 1
            if wk:
                w += 1
        print i,w
        if i == w:
            try:
                if self.args['group'] == "SinashowAvsgroup1":
                    replace('/srv/salt/Sinashow/AvsServer.sls',self.args['version'])
                elif self.args['group'] == "SinashowAvsgroup2":
                    replace('/srv/salt/Sinashow_one/AvsServer.sls',self.args['version'])
                elif self.args['group'] == "SinashowAvsgroup3":
                    replace('/srv/salt/Sinashow_two/AvsServer.sls',self.args['version'])
                elif self.args['group'] == "BusinessCrs":
                    replace('/srv/salt/Sinashow/ChatServer.sls',self.args['version'])
                elif self.args['group'] == "NobusinessCrs":
                    replace('/srv/salt/Sinashow_one/ChatServer.sls',self.args['version'])
                elif self.args['group'] == "FinanceCrs":
                    replace('/srv/salt/Sinashow_two/ChatServer.sls',self.args['version'])
                elif self.args['group'] == "SinashowTTgroup7":
                    replace('/srv/salt/Sinashow/TransTrans.sls',self.args['version'])
                elif self.args['group'] == "SinashowTTgroup8":
                    replace('/srv/salt/Sinashow_one/TransTrans.sls',self.args['version'])
                elif self.args['group'] == "FengBo_PhoneChat":
                    replace('/srv/salt/FengBo_PhoneChat/PhoneChatServer.sls',self.args['version'])
                else:
                    return 2
            except subprocess.CalledProcessError:
                return 3

            with open('/srv/pillar/schedule.sls', 'w') as sls:
                sls.write('schedule:\n')
                sls.write('  highstate:\n')
                sls.write('    function: state.highstate\n')
                sls.write('    minutes: 15\n')
            return True
        else:
            return 5


class TodoList(Resource):

    def post(self):
        args = parser_post.parse_args()
        # 构建新参数
        if args['user'] == "sa1t" and args['pwd'] == "saltstack":
            if args['group'] == "NobusinessCrs":
                fdir = '/srv/salt/Sinashow_one/'
            elif args['group'] == "FinanceCrs":
                fdir = '/srv/salt/Sinashow_two/'
            elif args['group'] == "FengBo_PhoneChat":
                fdir = '/srv/salt/FengBo_PhoneChat/'
            else:
                fdir = '/srv/salt/Sinashow/'
            oper = Async(args,fdir)
            if os.path.exists(fdir+'files/'+args['program']+'-'+args['version']+'.tar.gz'):
        # 调用方法to_do
                info = {"info": str(oper.excute())+"package already exists"}
        # # 资源添加成功，返回201
                return info,201
            else:
                info = {"info": oper.tarpkg()+oper.excute()}
                return info,201
        else:
            abort(400)

class SendList(Resource):

    def post(self):
        args = parser_post.parse_args()
        # 构建新参数
        if args['user'] == "sa1t" and args['pwd'] == "saltstack":
        # 调用方法to_do
            mail = SendMail(args)
            info = {"info": mail.send_mail()}
        # # 资源添加成功，返回201
            return info,201
        else:
            abort(400)


# 设置路由，即路由地址为http://127.0.0.1:5000/users
api.add_resource(TodoList, "/json")
api.add_resource(SendList, "/json")

if __name__ == '__main__':
    app.run(host='192.168.9.126',port='5000',debug=True)
