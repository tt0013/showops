#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: celery.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/9/5 18:42
"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery_proj' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showops.settings')
app = Celery('showops')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))