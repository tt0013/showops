import time
import os,base64
from django.http import JsonResponse
from django.shortcuts import render,render_to_response
from public.views import admin_required
from .models import *
from .mail import *
from .tasks import *
from django.db.models import Avg
from .Popularity import *
# Create your views here.


@admin_required
def fengbo_flow(request):
    startime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time() - 24 * 60 * 60 * 8)), "%Y%m%d")))
    # nowtime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time())), "%Y%m%d")))
    if request.method == 'POST':
        keyword = request.POST.get('keyword', None)
        addressee = request.POST.get('addressee', None)
        copyper = request.POST.get('copyper', None)
        dates = request.POST.get('dates', None)
        describe = request.POST.get('formulation', None)
        picone = request.POST.get('picone',None)
        pictwo = request.POST.get('pictwo',None)
        picthree = request.POST.get('picthree',None)

        if keyword:
            try:
                Time = time.mktime(time.strptime(dates.split(' - ')[0], "%Y-%m-%d"))
                if Fengbo_Bandwidth.objects.get(Dtime=Time).Wangsunum:
                    data = {'code': 1, 'msg': '数据已存在!'}
                else:
                    print(1)
                    banddata = FengBoactualData(dates.split(' - ')[0], dates.split(' - ')[1], keyword)
                    banddata.UpdateData()
                    data = {'code': 0, 'msg': '执行成功!'}
            except:
                try:
                    print(2)
                    banddata = FengBoactualData(dates.split(' - ')[0], dates.split(' - ')[1], keyword)
                    banddata.GetInsertData_Mssql()
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
                if fengbomail(addressee, copyper, describe):
                    data = {'code': 0, 'msg': '执行成功!'}
                else:
                    data = {"code": 1, "msg": '执行失败!'}
            except:
                data = {"code": 1, "msg": '执行失败!'}
        else:
            data = {"code": 1, "msg": '执行失败!'}
        return JsonResponse(data)

    elif request.method == 'GET':
        wid = FengBoactualData()
        widdata = wid.Popuwidth()
        try:
            obj = Fengbo_Bandwidth.objects.filter(Dtime__gt=startime).order_by('Dtime')
            dates, anum, aunum, vinum, wsnum, uwidth, dwidth = [], [], [], [], [], [], []
            for row in obj:
                if row.Wangsunum == None:
                    row.Wangsunum = 0
                dates.append((time.strftime("%m/%d", time.localtime(row.Dtime))) + " " + "星期" + row.Week)
                anum.append(row.Anchornum)
                aunum.append(row.Audionum)
                vinum.append(row.Videonum)
                wsnum.append(row.Wangsunum)
                uwidth.append(row.Upbindwidth)
                dwidth.append(row.Downbindwidth)
            Popu = {
                "dates": dates,
                "anum": anum,
                "aunum": aunum,
                "vinum": vinum,
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
def yiren_flow(request):
    startime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time() - 24 * 60 * 60 * 8)), "%Y%m%d")))
    if request.method == 'POST':
        dates = request.POST.get('dates', None)
        addressee = request.POST.get('addressee', None)
        copyper = request.POST.get('copyper', None)
        describe = request.POST.get('formulation', None)
        picone = request.POST.get('picone',None)
        pictwo = request.POST.get('pictwo',None)
        picthree = request.POST.get('picthree',None)

        if dates:
            banddata = YishowactualData(dates.split(' - ')[0], dates.split(' - ')[1])
            Time = time.mktime(time.strptime(dates.split(' - ')[0], "%Y-%m-%d"))
            if YiShow_Bandwidth.objects.filter(Dtime=Time).first() == None:
                banddata.GetInsertData_Mssql()
                data = {'code': 0, 'msg': '执行成功!'}
            else:
                data = {'code': 1, 'msg': '数据已存在!'}
        elif addressee:
            try:
                dicts = {
                    "image1": picone.split(",")[1].replace(" ", "+"),
                    "image2": pictwo.split(",")[1].replace(" ", "+"),
                    "image3": picthree.split(",")[1].replace(" ", "+"),
                }
                if not os.path.exists("E:\Django_Node\showops\\updatetask\echarts\images\YiShow\\"):
                    os.makedirs("E:\Django_Node\showops\\updatetask\echarts\images\YiShow\\")
                for k, v in dicts.items():
                    with open("E:\Django_Node\showops\\updatetask\echarts\images\YiShow\\" + k + ".png", "wb") as f:
                        f.write(base64.b64decode(v))
                if copyper == None:
                    copyper = ""
                elif describe == None:
                    describe = ""
                if yshowmail(addressee, copyper, describe):
                    data = {'code': 0, 'msg': '执行成功!'}
                else:
                    data = {"code": 1, "msg": '执行失败!'}
            except:
                data = {"code": 1, "msg": '执行失败!'}
        else:
            data = {"code": 1, "msg": '执行失败!'}
        return JsonResponse(data)

    elif request.method == 'GET':
        bw = YishowactualData()
        bwdata = bw.Popuwidth()
        try:
            obj = YiShow_Bandwidth.objects.filter(Dtime__gt=startime).order_by('Dtime')
            dates, minwd, moutwd, binwd, boutwd, buzznum, cdnwd = [], [], [], [], [], [], []
            for row in obj:
                dates.append((time.strftime("%m/%d", time.localtime(row.Dtime))) + " " + "星期" + row.Week)
                minwd.append(row.Motorinwidth)
                moutwd.append(row.Motoroutwidth)
                binwd.append(row.Bgpinwidth)
                boutwd.append(row.Bgpoutwidth)
                buzznum.append(row.Buzznum)
                cdnwd.append(row.Cdnwidth)
            Popu = {
                "dates": dates,
                "minwd": minwd,
                "moutwd": moutwd,
                "binwd": binwd,
                "boutwd": boutwd,
                "buzznum": buzznum,
                "cdnwd": cdnwd
            }
            return render(request, 'flow/yirenflows.html', {"bwdata": bwdata, "Popu": Popu})
        except:
            return render(request, 'flow/yirenflows.html', {"bwdata": bwdata})
    else:
        return render(request, 'flow/yirenflows.html')

@admin_required
def sinashow_flow(request):
    startime = int(time.mktime(time.strptime(time.strftime('%Y%m%d', time.localtime(time.time() - 24 * 60 * 60 * 8)), "%Y%m%d")))
    '''SinaShow'''
    get_7_daydata = SinaShow_Bandwidth.objects.filter(Time__gte=startime)
    Totals, Dates = [], []
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

        '''show 近一周流量'''
        SHOW_JiaXing, SHOW_BaoJi, SHOW_KS, SHOW_GanSu, SHOW_HG, SHOW_JinHua, SHOW_ChangZhi, SHOW_JinHua1, SHOW_JiaXing1 = [], [], [], [], [], [], [], [], []
        for line in get_7_daydata:
            SHOW_JiaXing.append(line.SHOW_JIAXING)
            SHOW_BaoJi.append(line.SHOW_BaoJi)
            SHOW_KS.append(line.SHOW_KS)
            SHOW_GanSu.append(line.SHOW_GanSu)
            SHOW_HG.append(line.SHOW_HG)
            SHOW_JinHua.append(line.SHOW_JinHua)
            SHOW_ChangZhi.append(line.SHOW_ChangZhi)
            SHOW_JinHua1.append(line.SHOW_JinHua1)
            SHOW_JiaXing1.append(line.SHOW_JiaXing1)

        '''近8周'''
        time_list = []
        get_fridatatime = SinaShow_Bandwidth.objects.filter(Week='五').order_by("-Time")[0:9]
        for mytime in get_fridatatime:
            time_list.append(mytime.Time)
        time_list.reverse()
        num = len(time_list)
        MaxTraffic_list = []
        for i in range(0, num):
            if i != num - 1:
                Max_traff = SinaShow_Bandwidth.objects.filter(Time__gte=time_list[i], Time__lte=time_list[i + 1]).aggregate(
                    Avg('Total'))
                MaxTraffic_list.append(int(Max_traff['Total__avg']))

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
        'Traffic': Traffic,
        'SHOW_JiaXing': SHOW_JiaXing,
        'SHOW_BaoJi': SHOW_BaoJi,
        'SHOW_KS': SHOW_KS,
        'SHOW_GanSu': SHOW_GanSu,
        'SHOW_HG': SHOW_HG,
        'SHOW_JinHua': SHOW_JinHua,
        'SHOW_ChangZhi': SHOW_ChangZhi,
        'SHOW_JinHua1': SHOW_JinHua1,
        'SHOW_JiaXing1': SHOW_JiaXing1,
        'MaxTraffic_list': MaxTraffic_list
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
    return render_to_response('flow/showflows.html', data)


