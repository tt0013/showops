#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,os,stat
import zipfile,tarfile
import shutil
import subprocess
# from replace import replace


result = subprocess.Popen("/usr/bin/salt -N FengBo_PhoneChat pillar.get schedule" ,shell=True,
                                      stdout=subprocess.PIPE)

print(result)


