#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import os

def modifystrategy(date):
    with open('updatetask/strategy/schedule.sls','w') as sls:
        sls.write("schedule:")
        sls.write("  highstate:")
        sls.write("    function: state.highstate")
        sls.write("    when:       %s     5:00am" % date)



