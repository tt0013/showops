#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,os,stat
import zipfile,tarfile
import shutil
import subprocess
from updatetask.replace import replace




class Async(object):
    def __init__(self,platform,program,group,week,version,ftpadd):
        self.platform = platform
        self.program = program
        self.group = group
        self.week = week
        self.version = version
        self.ftpadd = ftpadd
        self.pkgdir = 'pkg'
        self.Initialdir = os.getcwd()

    def tarpkg(self):
        zipf = self.ftpadd.split('/').pop()
        if os.path.exists(self.Initialdir + '/' + zipf):
            os.remove(self.Initialdir + '/' + zipf)
        ftp = subprocess.call("wget %s" % self.ftpadd, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        if ftp == 0:
            if os.path.isdir(self.Initialdir + '/' + self.pkgdir):
                 shutil.rmtree(self.Initialdir + '/' + self.pkgdir)
                 os.mkdir(self.pkgdir)
            zipf = self.Initialdir + '/' + zipf
            if self.program == "PhoneChatServer" or self.program == "AvsServer":
                 tar = tarfile.open(zipf, "r")
                 for f in tar:
                    tar.extract(f,self.Initialdir + '/' + self.pkgdir)
                 tar.close()
                 newfile = tarfile.open(self.program + '-' + self.version + '.tar.gz', "w:gz")
                 os.chdir(self.pkgdir)
                 for root, dir, files in os.walk(self.Initialdir + '/' + self.pkgdir):
                     for f in files:
                         os.chmod(self.Initialdir + '/' + self.pkgdir + '/' + f, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
                         newfile.add(f)
                 newfile.close()
                 nfile = self.Initialdir + '/' + self.program + '-' + self.version + '.tar.gz'
#                 try:
#                     shutil.move(nfile, '/srv/salt/FengBo_PhoneChat/files/')
#                     os.remove(zipf)
#                 except shutil.Error:
#                     return False
            else:
                 pkgzip = zipfile.ZipFile(zipf, 'r')
                 for f in pkgzip.namelist():
                     pkgzip.extract(f, self.Initialdir + '/' + self.pkgdir)
                     os.chmod(self.Initialdir + '/' + self.pkgdir + '/' + f, stat.S_IRWXU | stat.S_IXGRP | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
                 pkgzip.close()
                 newfile = tarfile.open(self.program + '-' + self.version + '.tar.gz', "w:gz")
                 os.chdir(self.pkgdir)
                 for root, dir, files in os.walk(self.Initialdir + '/' + self.pkgdir):
                     for f in files:
                         newfile.add(f)
                 newfile.close()
                 nfile = self.Initialdir + '/' + self.program + '-' + self.version + '.tar.gz'
            try:
                if self.group == "NobusinessCrs":
                    shutil.move(nfile, '/srv/salt/Sinashow_one/files/')
                elif self.group == "FinanceCrs":
                    shutil.move(nfile, '/srv/salt/Sinashow_two/files/')
                elif self.group == "FengBo_PhoneChat":
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

    def excute(self):
        i = 0
        w = 0
        with open('/srv/pillar/schedule.sls', 'w') as sls:
            sls.write('schedule:\n')
            sls.write('  highstate:\n')
            sls.write('    function: state.highstate\n')
            sls.write('    when:       %s     5:00am\n' % self.week)
        try:
            subprocess.check_call("/usr/bin/salt -N %s saltutil.refresh_pillar " % self.group, shell=True)
#            subprocess.call("/usr/bin/salt -N %s saltutil.refresh_pillar " % self.group, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
            result = subprocess.Popen("/usr/bin/salt -N %s pillar.get schedule" % self.group, shell=True,
                                      stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
#            return False
            print(1)
        for line in result.stdout.readlines():
            line = line.strip('\n')
            ip = re.search(r'(\d+\.){3}\d+', line)
            wk = re.search(r'^\s+%s\s+%s' % (self.week,'5:00am'), line)
            if ip:
                i += 1
            if wk:
                w += 1
        if i == w:
            try:
                if self.program == "AvsServer" and self.group == "SinashowAvsgroup1":
                    replace('/srv/salt/Sinashow/AvsServer.sls',self.version)
                elif self.program == "AvsServer" and self.group == "SinashowAvsgroup2":
                    replace('/srv/salt/Sinashow_one/AvsServer.sls',self.version)
                elif self.program == "AvsServer" and self.group == "SinashowAvsgroup3":
                    replace('/srv/salt/Sinashow_two/AvsServer.sls',self.version)
                elif self.program == "ChatServer" and self.group == "BusinessCrs":
                    replace('/srv/salt/Sinashow/ChatServer.sls',self.version)
                elif self.program == "ChatServer" and self.group == "NobusinessCrs":
                    replace('/srv/salt/Sinashow_one/ChatServer.sls',self.version)
                elif self.program == "ChatServer" and self.group == "FinanceCrs":
                    replace('/srv/salt/Sinashow_two/ChatServer.sls',self.version)
                elif self.program == "TransTrans" and self.group == "SinashowTTgroup7":
                    replace('/srv/salt/Sinashow/TransTrans.sls',self.version)
                elif self.program == "TransTrans" and self.group == "SinashowTTgroup8":
                    replace('/srv/salt/Sinashow_one/TransTrans.sls',self.version)
                elif self.program == "PhoneChatServer" and self.group == "FengBo_PhoneChat":
                    replace('/srv/salt/FengBo_PhoneChat/PhoneChatServer.sls',self.version)
                else:
#                    return False
                    print(2)
            except subprocess.CalledProcessError:
#                return False
                print(3)

            with open('/srv/pillar/schedule.sls', 'w') as sls:
                sls.write('schedule:\n')
                sls.write('  highstate:\n')
                sls.write('    function: state.highstate\n')
                sls.write('    minutes: 15\n')
#            return True
            print(4)
        else:
#            return False
            print(5)

def mains():
    salt = Async(
#        platform='FengBo',program='PhoneChatServer',group='FengBo_PhoneChat',week='Monday',version='0.0.93',ftpadd='ftp://liuyang:0wN2hFdV@ftp.intra.sinashow.com/AVS/AvsServer1.3.9.9.tar.gz'
        platform='FengBo',program='PhoneChatServer',group='FengBo_PhoneChat',week='Monday',version='0.0.93',ftpadd='ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/PhoneCRS/room_0.0.93.tar.gz'
#        platform='SinaShow',program='ChatServer',group='FinanceCrs',week='Monday',version='4.3.1.36',ftpadd='ftp://wangaiwei:277Mq5SW@ftp.intra.sinashow.com/show_crs/ChatServer_4.3.1.36.zip'
    )
#    salt.tarpkg()
    salt.excute()

if __name__ == '__main__':
    mains()






