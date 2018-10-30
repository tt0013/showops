import time,datetime
import json
from django.shortcuts import render
from updatetask.echarts.flow import Flowcount
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from public.views import Sendmail, user_serach, Menulist, admin_required, login_required

# Create your views here.

@admin_required
def flows_count(request):
    if request.method == 'POST':
        return JsonResponse('1')
    if request.method == 'GET':
        up = Flowcount('Up')
        down = Flowcount('Down')
        print(up['flow'])
        print(max(up['flow']))
        return render(request, 'proupdate/flows/add.html', {"up":up,"down":down})
    return render(request, 'proupdate/flows/add.html')

# @admin_required
# def flows_count(request):
#     if request.method == 'POST':
#         platform = request.POST.get('platform', None)
#         asdl = request.POST.get('asdl', None)
#         dates = request.POST.get('dates', None)
#         if platform and dates:
#             Saltgroup.objects.create(
#                 platform=platform,
#                 asdl=asdl,
#                 dates=dates,
#             )
#             messgs = {'code': 0, 'msg': '添加成功!'}
#         else:
#             messgs = {'code': 1, 'msg': '添加失败!'}
#         return JsonResponse(messgs)
#     else:
#         return render(request, 'itom/proupdate/flows/add.html')
