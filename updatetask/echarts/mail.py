#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os,time,smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart




def fengbomail(addressee,copyper=None,describe=None):
    from_addr = 'monitorshow@tiange.com'
    password = 'eOPD#A2I'
    smtp_server = 'mail.tiange.com'
    times = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24*60*60))

    msg = MIMEMultipart('mixed')
    content = MIMEText('<html><body><br><font size="4" color="red">  %s</font></br><img src="cid:image1.png"><img src="cid:image2.png"><img src="cid:image3.png"></body></html>' % describe, 'html', 'utf-8')
    msg.attach(content)


    msg['From'] = (u'FengBo Bandwidth <%s>' % from_addr)
    msg['To'] = addressee
    msg['Cc'] = copyper
    msg['Subject'] = Header(u'%s 疯播近七日流量' % times,'utf-8').encode()

    for root, dirs, files in os.walk("E:\Django_Node\showops\\updatetask\echarts\images\Fengbo"):
        for f in files:
            with open(root+"\\"+f,"rb") as fi:
                img = MIMEImage(fi.read())
                img.add_header('Content-ID', f)
                msg.attach(img)

    try:
        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, password)
        server.sendmail(from_addr, addressee.split(",") + copyper.split(","), msg.as_string())
        server.quit()
        return True
    except:
        return False




def showmail(addressee,copyper=None,describe=None):
    from_addr = 'monitorshow@tiange.com'
    password = 'eOPD#A2I'
    smtp_server = 'mail.tiange.com'
    times = time.strftime('%Y-%m-%d',time.localtime(time.time() - 24*60*60))

    msg = MIMEMultipart('related')
    content = MIMEText('<html><body><br><font size="4" color="red">  %s</font></br><img src="cid:imgbase1.png"><img src="cid:imgbase2.png"><img src="cid:imgbase3.png"><img src="cid:imgbase4.png"><img src="cid:imgbase5.png"></body></html>' % describe, 'html', 'utf-8')
    msg.attach(content)


    msg['From'] = (u'SinaShow Bandwidth <%s>' % from_addr)
    msg['To'] = addressee
    msg['Cc'] = copyper
    msg['Subject'] = Header(u'%s SHOW近七日流量' % times,'utf-8').encode()

    for root, dirs, files in os.walk("E:\Django_Node\showops\\updatetask\echarts\images\Sinashow"):
        for f in files:
            with open(root+"\\"+f,"rb") as fi:
                img = MIMEImage(fi.read())
                img.add_header('Content-ID', f)
                msg.attach(img)
    try:
        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, password)
        server.sendmail(from_addr, addressee.split(",") + copyper.split(","), msg.as_string())
        server.quit()
        return True
    except:
        return False

# if __name__ == '__main__':
#     fengbomail("yangtianqi@tiange.com","")
    # showmail("yangtianqi@tiange.com","")
