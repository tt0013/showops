#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi

import re


def replace(file_path,new_str):
    try:
        f = open(file_path, 'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){2,3}\d+')
            line = re.sub(pattern, new_str, line)
            f.write(line)
        f.close()
    except Exception:
        return False



