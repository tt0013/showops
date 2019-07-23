from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from public.views import admin_required
import requests,json

# Create your views here.


def ldapjoggle(ask, role, userid=None, email=None, gid=None, gecos=None, shell=None, ou=None):
    info = {
        'user': 'root',
        'pwd': 'openldap',
        'role': role,
        'userid': userid,
        'email': email,
        'gid': gid,
        'gecos': gecos,
        'shell': shell,
        'ou': ou
    }
    headers = {'content-type': 'application/json'}
    r = requests.post("http://183.131.72.144:3800/%s" % ask, data=json.dumps(info), headers=headers)
    result = json.loads(r.json())
    return result

def ldapsudo(ip, opt, seat):
    info = {
        'user': 'root',
        'pwd': 'ldapsudo',
        'ip': ip,
        'option': opt,
        'seat': seat
    }
    headers = {'content-type': 'application/json'}
    r = requests.post("http://192.168.9.18:3800/sudoauth", data=json.dumps(info), headers=headers)
    result = r.json()
    return result

@admin_required
def user_ldap(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = []
            for u in ldapjoggle('optldap', 'alluser'):
                if keyword in u['uid']:
                    org_list.append(u)
        else:
            org_list = ldapjoggle('optldap', 'alluser')
        paginator = Paginator(org_list, int(limit))
        data = [{"uid": n['uid'], "uidNumber":n['uidNumber'],"gidNumber":n['gidNumber'],
                 "gecos":n['gecos'],"objectClass": n['objectClass']} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)
    return render(request, 'ldap/user/index.html')

@admin_required
def useradd_ldap(request):
    gid_list = ldapjoggle('optldap', 'gid')
    if request.method == 'POST':
        userid = request.POST.get('userid', None)
        email = request.POST.get('email', None)
        gid = request.POST.get('gid', None)
        gecos = request.POST.get('gecos', None)
        shell = request.POST.get('shell', None)
        if userid and gid and gecos and shell and email:
            try:
                ldapjoggle('addldap','adduser',userid=userid,email=email,gid=gid,gecos=gecos,shell=shell)
                messgs = {'code': 0, 'msg': '执行成功!'}
            except:
                messgs = {'code': 1, 'msg': '执行失败!'}
        else:
            messgs = {'code': 1, 'msg': '执行失败!'}
        return JsonResponse(messgs)
    else:
        return render(request, 'ldap/user/add.html', {"groups": gid_list})

@admin_required
def userdel_ldap(request):
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        if uid:
            try:
                ldapjoggle('delldap', 'user', userid=uid)
                messgs = {'code': 0, 'msg': '修改成功!'}
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}

        return JsonResponse(messgs)


@admin_required
def usereset_ldap(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', None)
        email = request.POST.get('email', None)
        if email and uname:
            try:
                ldapjoggle('reldap','resetpass', userid=uname, email=email)
                messgs = {'code': 0, 'msg': '修改成功!'}
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}
        return JsonResponse(messgs)
    uname = request.GET.get('uname', None)
    return render(request, 'ldap/user/edit.html', locals())



@admin_required
def group_ldap(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = []
            for u in ldapjoggle('optldap','allgroup'):
                if keyword in u['cn']:
                    org_list.append(u)
        else:
            org_list = ldapjoggle('optldap','allgroup')
        paginator = Paginator(org_list, int(limit))
        data = [{"group": n['cn'], "gidNumber":n['gidNumber'],
                 "objectClass": n['objectClass']} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)

    return render(request, 'ldap/group/index.html')

@admin_required
def groupadd_ldap(request):
    if request.method == 'POST':
        group = request.POST.get('group', None)
        if group:
            try:
                ldapjoggle('addldap','addgroup',gecos=group)
                messgs = {'code': 0, 'msg': '执行成功!'}
            except:
                messgs = {'code': 1, 'msg': '执行失败!'}
        else:
            messgs = {'code': 1, 'msg': '执行失败!'}
        return JsonResponse(messgs)
    else:
        return render(request, 'ldap/group/add.html')

@admin_required
def groupdel_ldap(request):
    if request.method == 'POST':
        group = request.POST.get('group', None)
        if group:
            try:
                ldapjoggle('delldap', 'group', gecos=group)
                messgs = {'code': 0, 'msg': '修改成功!'}
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}

        return JsonResponse(messgs)


@admin_required
def ou_ldap(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = []
            for u in ldapjoggle('optldap','allou'):
                if keyword in u['ou']:
                    org_list.append(u)
        else:
            org_list = ldapjoggle('optldap','allou')
        paginator = Paginator(org_list, int(limit))
        data = [{"ou": n['ou'], "objectClass": n['objectClass']} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)

    return render(request, 'ldap/ou/index.html')

@admin_required
def ouadd_ldap(request):
    if request.method == 'POST':
        ou = request.POST.get('ou', None)
        if ou:
            try:
                ldapjoggle('addldap','addou',ou=ou)
                messgs = {'code': 0, 'msg': '执行成功!'}
            except:
                messgs = {'code': 1, 'msg': '执行失败!'}
        else:
            messgs = {'code': 1, 'msg': '执行失败!'}
        return JsonResponse(messgs)
    else:
        return render(request, 'ldap/ou/add.html')

@admin_required
def oudel_ldap(request):
    if request.method == 'POST':
        ou = request.POST.get('ou', None)
        if ou:
            try:
                ldapjoggle('delldap', 'ou', ou=ou)
                messgs = {'code': 0, 'msg': '修改成功!'}
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}

        return JsonResponse(messgs)

@admin_required
def sudo_ldap(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = []
            for u in ldapjoggle('optldap', 'alluser'):
                if keyword in u['uid']:
                    org_list.append(u)
        else:
            org_list = ldapjoggle('optldap', 'alluser')
        paginator = Paginator(org_list, int(limit))
        data = [{"uid": n['uid'],"gecos":n['gecos']} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)
    return render(request, 'ldap/sudo/index.html')

@admin_required
def sudoadd_ldap(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', None)
        opts = request.POST.get('opts', None)
        rule = request.POST.get('rule', None)
        ldapgroup = request.POST.get('ldapgroup', None)
        if ip and opts and rule and ldapgroup:
            try:
                opt = "%{0}    {1}".format(ldapgroup.split(" ")[0], opts)
                messgs = ldapsudo(ip, opt, rule)
                # messgs = {'code': 0, 'msg': '修改成功!'}
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}
        return JsonResponse(messgs)
    ldapgroup = request.GET.get('ldapgroup', None)
    return render(request, 'ldap/sudo/add.html', locals())

@admin_required
def sudodel_ldap(request):
    if request.method == 'POST':
        ip = request.POST.get('ip', None)
        rule = request.POST.get('rule', None)
        ldapgroup = request.POST.get('ldapgroup', None)
        if ip and rule and ldapgroup:
            try:
                opt = "%{0}    {1}".format(ldapgroup.split(" ")[0], None)
                messgs = ldapsudo(ip, opt, rule)
            except:
                messgs = {'code': 1, 'msg': '修改失败!'}
        else:
            messgs = {'code': 1, 'msg': '修改失败!'}
        return JsonResponse(messgs)
    ldapgroup = request.GET.get('ldapgroup', None)
    return render(request, 'ldap/sudo/del.html', locals())