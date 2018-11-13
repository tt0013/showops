from django.shortcuts import render
import time,datetime
import os,base64
from updatetask.Popularity import AnalysisData
from django.http import JsonResponse
from django.shortcuts import render,render_to_response
from public.views import Sendmail, user_serach, Menulist, admin_required, login_required
from .models import *
from updatetask.echarts.mail import fengbomail,showmail
# Create your views here.


def user_ldap(request):
    return