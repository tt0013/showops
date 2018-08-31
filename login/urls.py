#!usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Author:LiJie
@Mail: lijie2402@sina.cn
@File: urls.py
@Time: 2018/08/29
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/', views.Login.as_view(), name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^vercode/', views.Verification, name="vercode"),
    # url(r'^userinfo/(?P<id>\d+)$', views.UserInfo.as_view(), name="userinfo"),
    # url(r'^password/', views.UserInfo.password, name="password"),
]

