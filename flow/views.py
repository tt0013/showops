import time
import os,base64
from updatetask.Popularity import AnalysisData
from django.http import JsonResponse
from django.shortcuts import render,render_to_response
from public.views import Sendmail, user_serach, Menulist, admin_required, login_required
from .models import *
from updatetask.echarts.mail import *
# Create your views here.


startime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time() - 24 * 60 * 60 * 8)), "%Y%m%d")))

@admin_required
def fengbo_flow(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', None)
        addressee = request.POST.get('addressee', None)
        copyper = request.POST.get('copyper', None)
        describe = request.POST.get('formulation', None)
        picone = request.POST.get('picone',None)
        pictwo = request.POST.get('pictwo',None)
        picthree = request.POST.get('picthree',None)

        if keyword:
            try:
                Time = time.mktime(
                    time.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)), "%Y-%m-%d"))
                if Fengbo_Bandwidth.objects.filter(Dtime=Time).all():
                    data = {'code': 1, 'msg': '数据存在,操作重复!'}
                else:
                    wid = AnalysisData()
                    wid.InsertData(keyword)
                    data = {'code': 0, 'msg': '执行成功!'}
            except:
                data = {"code": 1, "msg": '执行失败!'}
        elif addressee:
            try:
                dicts = {
                    "image1": picone.split(",")[1].replace(" ", "+"),
                    "image2": pictwo.split(",")[1].replace(" ", "+"),
                    "image3": picthree.split(",")[1].replace(" ", "+"),
                }
                if not os.path.exists("E:\Django_Node\showops\\updatetask\echarts\images\FengBo\\"):
                    os.makedirs("E:\Django_Node\showops\\updatetask\echarts\images\FengBo\\")
                for k, v in dicts.items():
                    with open("E:\Django_Node\showops\\updatetask\echarts\images\FengBo\\" + k + ".png", "wb") as f:
                        f.write(base64.b64decode(v))
                if copyper == None:
                    copyper = ""
                elif describe == None:
                    describe = ""
                if fengbomail(addressee,copyper,describe):
                    data = {'code': 0, 'msg': '执行成功!'}
                else:
                    data = {"code": 1, "msg": '执行失败!'}
            except:
                data = {"code": 1, "msg": '执行失败!'}
        else:
            data = {"code": 1, "msg": '执行失败!'}
        return JsonResponse(data)

    elif request.method == 'GET':
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fromday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        tm = time.strftime('%H:%M:%S',time.localtime(time.time()))
        wid = AnalysisData()
        widdata = wid.Popuwidth(fromday+"T10:00:00",today+"T"+tm)
        try:
            obj = Fengbo_Bandwidth.objects.filter(Dtime__gt=startime)
            dates, unum, anum, wsnum, uwidth, dwidth = [], [], [], [], [], []
            for row in obj:
                if row.Wangsunum == None:
                    row.Wangsunum = 0
                dates.append((time.strftime("%m/%d", time.localtime(row.Dtime))) + " " + "星期" + row.Week)
                unum.append(row.Usernum)
                anum.append(row.Anchornum)
                wsnum.append(row.Wangsunum)
                uwidth.append(row.Upbindwidth)
                dwidth.append(row.Downbindwidth)
            Popu = {
                "dates": dates,
                "unum": unum,
                "anum": anum,
                "wsnum": wsnum,
                "uwidth": uwidth,
                "dwidth": dwidth
            }
            return render(request, 'flow/fengboflows.html', {"widdata": widdata, "Popu": Popu})
        except:
            return render(request, 'flow/fengboflows.html', {"widdata": widdata})
    else:
        return render(request, 'flow/fengboflows.html')


@admin_required
def sinashow_flow(request):
    '''SinaShow'''
    get_7_daydata = SinaShow_Bandwidth.objects.filter(Time__gte=startime)
    Totals,Dates = [],[]
    for i in get_7_daydata:
        Day = time.strftime('%m.%d', time.localtime(i.Time)) + " (星期%s)" %  i.Week
        Dates.append(Day)
        Totals.append(int(i.Total))

    '''SinaShow_MaxUserTraffic'''
    SinaShow_MaxUserTrafficdata = SinaShow_MaxUserTraffic.objects.filter(Time__gte=startime)
    after_times,morn_times,after_usernum,morn_usernum,after_traff,morn_traff = [],[],[],[],[],[]
    for line in SinaShow_MaxUserTrafficdata :
        mytime = time.strftime('%m/%d', time.localtime(line.Time)) +  " " + line.morn_time  +"(星期%s)" % line.Week
        morn_times.append(mytime)
        morn_usernum.append(int(line.morn_useridnum))
        morn_traff.append(int(line.morn_traffic))
        mytime1 = time.strftime('%m/%d', time.localtime(line.Time)) + " " + line.after_time  + "(星期%s)" % line.Week
        after_times.append(mytime1)
        after_usernum.append(int(line.after_useridnum))
        after_traff.append(int(line.after_traffic))




    '''SinaShow_AvsUser'''
    SinaShow_AvsUserdata = SinaShow_AvsUser.objects.filter(Time__gte=startime)
    Point_times, Avs_Big_Num, Avs_Over_Num, Avs_General_Num, Mic_Big_Num, Mic_Over_Num,Mic_General_Num,Mic_Vip_Num,Traffic = [], [], [], [], [], [], [], [], []
    for Avsdata in SinaShow_AvsUserdata:
        Pointt = time.strftime('%m/%d', time.localtime(Avsdata.Time)) + " " + Avsdata.PointTime + " (星期%s)" % Avsdata.Week
        Point_times.append(Pointt)
        Avs_Big_Num.append(int(Avsdata.Avs_Big_Num))
        Avs_Over_Num.append(int(Avsdata.Avs_Over_Num))
        Avs_General_Num.append(int(Avsdata.Avs_General_Num))
        Mic_Big_Num.append(int(Avsdata.Mic_Big_Num))
        Mic_Over_Num.append(int(Avsdata.Mic_Over_Num))
        Mic_General_Num.append(int(Avsdata.Mic_General_Num))
        Mic_Vip_Num.append(int(Avsdata.Mic_Vip_Num))
        Traffic.append(int(Avsdata.Traffic))

    data =  {
        'Total_list': Totals,
        'Dates': Dates,
        'morn_times': morn_times,
        'morn_usernum': morn_usernum,
        'morn_traff': morn_traff,
        'after_times': after_times,
        'after_usernum': after_usernum,
        'after_traff': after_traff,
        'Point_times': Point_times,
        'Avs_Big_Num': Avs_Big_Num,
        'Avs_Over_Num': Avs_Over_Num,
        'Avs_General_Num': Avs_General_Num,
        'Mic_Big_Num': Mic_Big_Num,
        'Mic_Over_Num': Mic_Over_Num,
        'Mic_General_Num': Mic_General_Num,
        'Mic_Vip_Num': Mic_Vip_Num,
        'Traffic': Traffic
    }

    if request.method == 'POST':
        Recipients = request.POST.get('Recipients', None)
        CopySender = request.POST.get('CopySender', None)
        Describe = request.POST.get('formulation', None)

        imgbase1 = request.POST.get('imgbase1', None)
        imgbase2 = request.POST.get('imgbase2', None)
        imgbase3 = request.POST.get('imgbase3', None)
        imgbase4 = request.POST.get('imgbase4', None)
        imgbase5 = request.POST.get('imgbase5', None)
        try:
            dicts = {
                "imgbase1": imgbase1.split(",")[1].replace(" ", "+"),
                "imgbase2": imgbase2.split(",")[1].replace(" ", "+"),
                "imgbase3": imgbase3.split(",")[1].replace(" ", "+"),
                "imgbase4": imgbase4.split(",")[1].replace(" ", "+"),
                "imgbase5": imgbase5.split(",")[1].replace(" ", "+"),
            }
            if not os.path.exists("E:\Django_Node\showops\\updatetask\echarts\images\Sinashow\\"):
                os.makedirs("E:\Django_Node\showops\\updatetask\echarts\images\Sinashow\\")
            for k, v in dicts.items():
                with open("E:\Django_Node\showops\\updatetask\echarts\images\Sinashow\\" + k + ".png", "wb") as f:
                    f.write(base64.b64decode(v))
            if Describe == None:
                Describe = ""
            elif CopySender == None:
                CopySender = ""
            if showmail(Recipients,CopySender,Describe):
                data = {'code': 0, 'msg': '执行成功!'}
            else:
                data = {"code": 1, "msg": '执行失败!'}
        except:
            data = {"code": 1, "msg": '执行失败!'}
        return JsonResponse(data)
    else:
        return render_to_response('flow/showflows.html', data)


