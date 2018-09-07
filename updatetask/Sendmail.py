#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os,smtplib,configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from updatetask.CreateHtml import CreateHtml


class SendMail(object):
    def __init__(self,platform,program,group,day,title,file=None):
        self.username = 'monitor@sinashow.com'
        self.passwd = 'monitor'
        # self.recv = ['yangtianqi@sinashow.com','tt06090013@163.com']
        self.recv = ['yangtianqi@sinashow.com']
        self.platform = platform
        self.program = program
        self.group = group
        self.day = day
        self.title = title
        self.file = file
        self.email_host = 'mail.sinashow.com'
        self.port = 25

    def send_mail(self):
        msg = MIMEMultipart()
        #发送内容的对象
        if self.file:#处理附件的
            html = open(self.file,'r',encoding='utf-8').read()
            html_part = MIMEText(html, 'html', 'utf-8')
            msg.attach(html_part)
        msg['Subject'] = self.title  # 邮件主题
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
            conf.set('MAIL', 'platform', self.platform)
            conf.set('MAIL', 'program', self.program)
            conf.set('MAIL', 'group', self.group)
            conf.set('MAIL', 'date', self.day)
            conf.set('MAIL', 'state', '1')
            with open(r'E:\Django_Node\showops\updatetask\CreateHtml\mail.ini', "w",encoding='utf-8') as f:
                conf.write(f)

        except Exception:
            print("Fail")
            # return "Fail"
        else:
            return "Successd"

    def __del__(self):
        self.smtp.quit()

def execute(platform,program,group,day):
    # filename = os.getcwd()+"\CreateHtml\CreateHtml.html"
    filename = r'E:\Django_Node\showops\updatetask\CreateHtml\CreateHtml.html'
    try:
        CreateHtml.CreateHtml(filename, platform, program, day)
    except Exception:
        print("Fail")
    if platform == 'SinaShow':
        Title = u'[重要通知]-[程序更新]-[SHOW平台程序更新]-[%s]' % day
    else:
        Title = u'[重要通知]-[程序更新]-[疯播平台程序更新]-[%s]' % day
    m = SendMail(
        platform, program, group, day, title=Title, file=filename
    )
    return m.send_mail()


