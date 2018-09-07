#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os,re
import subprocess
import datetime

today = datetime.date.today()

def CreateHtml(filename,platform,program,day,group=None):
    with open(filename,"w+",encoding='utf-8') as page:
        page.write('<STYLE type="text/css"></STYLE>\n')
        page.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
        page.write('<html>\n')
        page.write('<head>\n')
        page.write('<meta charset="UTF-8">\n')
        page.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        page.write('<title>Program Mail</title>\n')
        page.write('</head>\n')
        page.write('<body style="margin:0;padding:0;">\n')
        page.write('<table cellspacing="0" cellpadding="0" width="100%" style="min-height:69px;border:1px #ADADAD solid;border-top-width:6px;font-family:Microsoft Yahei,sans-serif;font-size:14px;">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<td align="center">\n')
        page.write('<div style="text-align:left;max-width:730px;min-height:99px;">\n')
        page.write('<div style="float:left;height:69px;">\n')
        page.write('<a href="http://www.jiankongbao.com" target="_blank" style="display:block;height:42px;width:131px;margin:13px 20px 0;">\n')
        if platform == 'FengBo':
            page.write('<img style="height:82px;width:131px;" src="http://live.sinashow.com/images/pc/logo.png" alt="疯播LIVE" title="疯播LIVE"/>\n')
        else:
            page.write('<img style="border:none;" src="http://i3.sinaimg.cn/uc/sinashow4.0/2/logo.gif" alt="新浪SHOW" title="新浪SHOW"/>\n')
        page.write('</a></div></div></td></tr></tbody></table>\n')
        page.write('<table cellspacing="0" cellpadding="0" width="100%" style="border:1px #ADADAD solid;border-width:0 1px 0 1px;font-family:Microsoft Yahei,sans-serif;font-size:13px;">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<td align="center">\n')
        page.write('<div style="max-width:730px;text-align:left;border-bottom:1px #ADADAD dashed;min-height:500px;padding-bottom:20px;font-size:13px;">\n')
        page.write('<table width="100%" cellspacing="0" cellpadding="5">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<td>\n')
        page.write('<div style="border-bottom:1px #ADADAD solid;font-size:18px;line-height:40px;color:#28ab17;">服务器维护更新通知<span style="color:#28ab17;font-size:14px;"></span></div>\n')
        page.write('<p style="text-indent:24px;line-height:24px;font-size:13px;">相关业务同事您好：由Show运维负责的服务器维护将要维护，详细信息如下，请注意查看。其中故障处理技术支持的同事是24小时正常工作。如有问题，请大家发送电子邮件：yangtianqi@sinashow.com 或者 showit@sinashow.com。</p>\n')
        page.write('</td></tr>\n')
        page.write('<td>\n')
        page.write('<table width="100%" cellpadding="0" cellspacing="0">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<td style="height:10px;line-height:10px;">\n')
        page.write('<div style="color:#7bb009;font-size:11px;float:left;">\n')
        page.write('<tr>\n')
        page.write('<td>\n')
        page.write('<div style="border-bottom:1px #ADADAD solid;font-size:13px;line-height:30px;color:#28ab17;">程序版本信息<span style="color:#28ab17;font-size:13px;"></span></div>\n')
        page.write('<table width="100%" cellpadding="9" cellspacing="0" style="text-align:center;border:1px #929292 solid;font-size:13px;">\n')
        page.write('<thead>\n')
        page.write('<tr style="background:#929292;color:#FFF;">\n')
        page.write('<th>Update IP</th>\n')
        page.write('<th>Program Name</th>\n')
        page.write('<th>Update Time</th>\n')
        page.write('<th>Program Version Number</th>\n')
        page.write('</tr></thead>\n')
        # with open('mgversion','w+') as f:
        #     f.write(subprocess.getoutput("/usr/bin/salt -N %s grains.item %s" % (group,platform))+'\n'+str(today))
        with open('E:\PyCharmScripts\CMDB\AsyncTask\mail\mgversion','r') as f:
            for lists in f.readlines():
                if re.findall(r'(\d|None|Minion)', lists):
                    ips = lists.split(':')
                    for table in ips:
                        if re.search(r'^\d+', table):
                            ip = table
                        elif re.search(r'\S', table):
                            version = table.strip()
                            page.write('<tbody><tr><td><p style="color:#33ccff;font-weight:bold;">%s</p></td>\n' % ip)
                            page.write('<td><p style="color:#33ccff;font-weight:bold;">%s</p></td>\n' % program)
                            page.write('<td><p style="color:#33ccff;font-weight:bold;">%s</p></td>\n' % day)
                            page.write('<td><p style="color:#33ccff;font-weight:bold;">%s</p></td>\n' % version)
        page.write('</tr></tbody></table></td></tr></tbody></table></td></tbody></table></div></td></tr></tbody></table>\n')
        page.write('<table cellspacing="0" cellpadding="0" width="100%" style="border:1px #ADADAD solid;border-top:none;font-family:Microsoft Yahei,sans-serif;font-size:12px;line-height:35px;padding-bottom:30px;">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<table cellpadding="0" cellspacing="0" style="color:#989898;margin:0 auto;margin-top:10px;text-align:center;font-size:12px;">\n')
        page.write('<tbody>\n')
        page.write('<tr>\n')
        page.write('<td>\n')
        if platform == 'FengBo':
            page.write('<a style="color:#989898;" href="www.sinashow.com" target="_blank"> 疯播LIVE</a>\n')
        else:
            page.write('<a style="color:#989898;" href="www.sinashow.com" target="_blank"> 新浪SHOW</a>\n')
        page.write('</td></tr></tbody></table></tr></tbody></table>\n')
        page.write('</body>\n')
        page.write('</html>\n')


    return os.getcwd()








