#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yang Tian Qi


from celery import shared_task
import logging
from celery.utils.log import get_task_logger
from updatetask.Async import mains

# @shared_task
# def mains():
