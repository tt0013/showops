#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import time,smtplib,configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from updatetask.CreateHtml import CreateHtml
class SendMail(object):
    def __init__(self,platform,program,group,day,title,file=None):
        self.username = 'monitor@sinashow.com'
        self.passwd = 'monitor'
        self.recv = 'yangtianqi@sinashow.com'
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
            html = open(self.file).read()
            html_part = MIMEText(html, 'html', 'utf-8')
            msg.attach(html_part)
        if not isinstance(self.title, unicode):
            self.title = unicode(self.title, 'utf-8')
        # msg.attach(MIMEText(self.content,'plain', 'utf-8'))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = 'Automation Program <%s>' % self.username  # 发送者账号
        msg['To'] = self.recv  # 接收者账号列表
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
            conf.set('MAIL', 'state', 1)
            with open('E:\Django_Node\showops\updatetask\CreateHtml\mail.ini', "w") as f:
                conf.write(f)

        except Exception as e:
            return "Fail"
        else:
            return "Successd"

    def __del__(self):
        self.smtp.quit()

def main():
    CreateHtml('E:\Django_Node\showops\updatetask\CreateHtml\mail.ini','SinaShow','')
    mail = SendMail()

if __name__ == '__main__':
    main()
