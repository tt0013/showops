#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: urls.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/8/23 15:22
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^$", views.index),
    # url(r"^test/", views.test),
    # url(r"^login/$", views.login, name="login"),
    url(r"^home/$", views.home, name="home"),
    # url(r"^Verification/gt$", views.Verification, name="vergt"),
    #部门管理
    url(r"^org/", views.org, name="org"),
    url(r"^orgadd/", views.org_add, name="orgadd"),
    url(r"^orgedit/(?P<id>\d+)$", views.org_edit, name="orgedit"),
    url(r"^orgdel/", views.org_del, name="orgdel"),
    #权限组管理
    url(r"^group/", views.group, name="group"),
    url(r"^groupadd/", views.group_add, name="groupadd"),
    url(r"^groupedit/(?P<id>\d+)$", views.group_edit, name="groupedit"),
    url(r"^groupdel/", views.group_del, name="groupdel"),
    url(r"^groupauth/(?P<id>\d+)$", views.group_auth, name="groupauth"),
    url(r"^authjson/(?P<id>\d+)$", views.group_auth_json, name="authjson"),
    #用户管理
    url(r"^user/", views.user, name="user"),
    url(r"^useradd/", views.user_add, name="useradd"),
    url(r"^useredit/(?P<id>\d+)$", views.user_edit, name="useredit"),
    url(r"^userdel/", views.user_del, name="userdel"),
    url(r"^userreset/", views.user_reset, name="userreset"),
    url(r'^userinfo/(?P<id>\d+)$', views.UserInfo.as_view(), name="userinfo"),
    url(r'^password/', views.UserInfo.password, name="password"),
    #菜单管理
    url(r"^menu/", views.menu, name="menu"),
    url(r"^menuadd/", views.menu_add, name="menuadd"),
    url(r"^menuedit/(?P<id>\d+)$", views.menu_edit, name="menuedit"),
    url(r"^menudel/", views.menu_del, name="menudel"),
    #程序更新
    # url(r"^upmail/", views.upmail, name="upmail"),
    url(r"^updatemail/", views.update_mail, name="updatemail"),
    url(r"^upexecute/", views.up_execute, name="upexecute"),
]