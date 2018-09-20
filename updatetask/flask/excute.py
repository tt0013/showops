#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re,subprocess

week = 'Monday'
group = 'FinanceCrs'
i = 0
w = 0
with open('/srv/pillar/schedule.sls', 'w') as sls:
    sls.write('schedule:\n')
    sls.write('  highstate:\n')
    sls.write('    function: state.highstate\n')
    sls.write('    when:       %s     5:00am\n' % week)
try:
    subprocess.check_call("/usr/bin/salt -N %s saltutil.refresh_pillar " % group, shell=True)
#            subprocess.call("/usr/bin/salt -N %s saltutil.refresh_pillar " % self.group, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
    result = subprocess.Popen("/usr/bin/salt -N %s pillar.get schedule" % group, shell=True,
                              stdout=subprocess.PIPE)
except subprocess.CalledProcessError:
    print(1)
for line in result.stdout.readlines():
    line = line.strip('\n')
    ip = re.search(r'(\d+\.){3}\d+', line)
    wk = re.search(r'^\s+%s\s+%s' % (week,'5:00am'), line)
    if ip:
        i += 1
    if wk:
        w += 1
print(i,w)
