#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os
import smtplib
import datetime
from time import strftime, localtime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart



################################
from_addr = 'monitorshow@tiange.com'
password = 'eOPD#A2I'
to_addr = ["yangtianqi@tiange.com"]
smtp_server = 'mail.tiange.com'
times = strftime("%Y-%m-%d %H:%M",localtime())
################################

msg=MIMEMultipart()
msg['From'] = (u'Automation Program <%s>' % from_addr)
msg['To'] = ";".join(to_addr)
msg['Subject'] = Header(u'[重要通知]-[程序更新]-[SHOW平台程序更新]-''[%s]' % times,'utf-8').encode()
html_part = MIMEText('nihao','plain','utf-8')
msg.attach(html_part)

server = smtplib.SMTP(smtp_server, 25)
#server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
