"""showops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r"^$", views.index),
    # ldap用户
    url(r"^userldap/", views.user_ldap, name="userldap"),
    url(r"^ldapuseradd/", views.useradd_ldap, name="ldapuseradd"),
    url(r"^ldapuserdel/", views.userdel_ldap, name="ldapuserdel"),
    url(r"^ldapuserreset/", views.usereset_ldap, name="ldapuserreset"),
    # ldap用户组
    url(r"^groupldap/", views.group_ldap, name="groupldap"),
    url(r"^ldapgroupadd/", views.groupadd_ldap, name="ldapgroupadd"),
    url(r"^ldapgroupdel/", views.groupdel_ldap, name="ldapgroupdel"),
    # ldap组织单元
    url(r"^ouldap/", views.ou_ldap, name="ouldap"),
    url(r"^ouadd/", views.ouadd_ldap, name="ouadd"),
    url(r"^oudel/", views.oudel_ldap, name="oudel"),
    # ldap sudo权限
    url(r"^ldapsudo/", views.sudo_ldap, name="ldapsudo"),
    url(r"^ldapsudoadd/", views.sudoadd_ldap, name="ldapsudoadd"),
    url(r"^ldapsudodel/", views.sudodel_ldap, name="ldapsudodel"),
]

