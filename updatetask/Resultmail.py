#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import time,configparser
from updatetask.CreateHtml import CreateHtml
from updatetask.Sendmail import SendMail


conf = configparser.ConfigParser()
conf.read(r'E:\Django_Node\showops\updatetask\CreateHtml\mail.ini')

class Result(object):
    def __init__(self):
        self.platform = conf.get('MAIL','platform')
        self.program = conf.get('MAIL','program')
        self.group = conf.get('MAIL','group')
        self.date = time.strftime("%Y-%m-%d", time.localtime())
        self.state = conf.get('MAIL','state')
        self.filename = r'E:\Django_Node\showops\updatetask\CreateHtml\mail.ini'


    def send(self):
            CreateHtml.CreateHtml(self.filename,self.platform,self.program,self.date)
            if self.platform == 'SinaShow':
                Title = u'[重要通知]-[程序更新]-[SHOW平台程序更新]-[%s]' % self.date
            else:
                Title = u'[重要通知]-[程序更新]-[疯播平台程序更新]-[%s]' % self.date
            m = SendMail(
                self.platform, self.program, self.group, self.date, title=Title, file=self.filename
            )
            m.send_mail()


if __name__ == '__main__':
    #if conf.get('MAIL','state') == '1':
    for s in conf.sections():
        if conf.getint(s,'state') == 1:
            m = Result()
            m.send()
            conf.set(s, 'state', 0)
            conf.write(open(r'E:\PycharmScript\CMDB\showops\updatetask\CreateHtml\mail.ini','w',encoding='utf-8'))
        else:
            break
