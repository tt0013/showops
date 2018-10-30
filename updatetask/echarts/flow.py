#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import json
import time,datetime
from urllib import parse
from updatetask.echarts.Popularity import OpenApiDemo

c ={}
l = []
a =OpenApiDemo()
b =a.Flowcount()
print(b)