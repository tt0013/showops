from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Org, Group, Menu, Renewmail ,Async
import json,requests
from public.views import Sendmail, user_serach, Menulist, admin_required, login_required
# Create your views here.

@login_required
def index(request):
	tree = Menulist.condition_to_tree(request.session.get('uid'))
	#处理隐藏菜单
	#data = [t for t in tree if int(t['hide']) == 0]
	strtree = Menulist.glist_to_tree(tree)

	return render(request, 'itom/index.html', {'strtree': strtree})

@login_required
def home(request):
	return  render(request, 'itom/home.html')

@admin_required
def org(request):
	'''
	获取所有部门信息，POST请求利用paginator进行分页，
	并且写好前端插件所需的data格式数据，以json格式返回
	:param request:
	:return:
	'''
	if request.method == 'POST':
		page = request.POST.get('page', 1)
		limit = request.POST.get('limit', 10)
		keyword =request.POST.get('keyword', None)
		if keyword:
			org_list = Org.objects.filter(name=keyword)
		else:
			org_list = Org.objects.all()
		paginator = Paginator(org_list, int(limit))
		data = [{"id": n.id, "name": n.name, "describe": n.describe} for n in paginator.page(int(page)).object_list]
		data = {
			"code": 0,
			"msg": "",
			"count": paginator.count,
			"data": data,
		}
		return JsonResponse(data)

	return render(request, 'itom/org/index.html')

@admin_required
def org_add(request):
	'''
	部门添加，并且将添加成功或失败的结果，以json格式返回给前端
	:param request:
	:return:
	'''
	if request.method == 'POST':
		name = request.POST.get('name', None)
		describe = request.POST.get('describe', None)
		if name and describe:
			Org.objects.create(
				name=name,
				describe=describe,
			)
			messgs = {'code': 0, 'msg': '添加成功!'}
		else:
			messgs = {'code': 1, 'msg': '添加失败!'}
		return JsonResponse(messgs)

	return render(request, 'itom/org/add.html')

@admin_required
def org_edit(request, id):
	'''
	GET获取对应部门信息, POST部门描述信息修改，
	并将修改成功或失败的结果以json格式返回给前端
	:param request:
	:param id:
	:return:
	'''
	if request.method == 'POST':
		describe = request.POST.get('describe', None)
		if describe:
			Org.objects.filter(id=id).update(describe=describe)
			messgs = {'code': 0, 'msg': '修改成功!'}
		else:
			messgs = {'code': 1, 'msg': '修改失败!'}
		return HttpResponse(json.dumps(messgs), content_type="application/json")

	data = Org.objects.filter(id=id).first()
	return render(request, 'itom/org/edit.html', {"data": data})

@admin_required
def org_del(request):
	'''
	删除对应部门，并将删除成功或失败的结果，以json格式返回给前端
	:param request:
	:return:
	'''
	if request.method == 'POST':
		id = request.POST.get('id', None)
		if id:
			Org.objects.filter(id=id).delete()
			messgs = {'code': 0, 'msg': '删除成功!'}
		else:
			messgs = {'code': 1, 'msg': '删除失败!'}

		return JsonResponse(messgs)

@admin_required
def group(request):
	'''
	角色管理，通过layuiadmin封装好的异步通过post调用获取分页数据，
	如果有查询请求，会更具搜索添加进行分页返回数据
	:param request:
	page: 页数
	limit: 每页多少数据
	keyword: 查询条件，角色名
	:return:
	'''
	if request.method == 'POST':
		page = request.POST.get('page', 1)
		limit = request.POST.get('limit', 10)
		keyword =request.POST.get('keyword', None)
		if keyword:
			group_list = Group.objects.filter(name=keyword)
		else:
			group_list = Group.objects.all()
		paginator = Paginator(group_list, int(limit))
		data = [{"id": n.id, "name": n.name, "status": n.status,"describe": n.describe} \
				for n in paginator.page(int(page)).object_list]
		data = {
			"code": 0,
			"msg": "",
			"count": paginator.count,
			"data": data,
		}
		return JsonResponse(data)

	return render(request, 'itom/group/index.html')

@admin_required
def group_add(request):
	'''
	角色添加，post传递添加数据
	:param request:
	name: 角色名
	status: 角色状态（0表示禁用，1表示启用）
	describe: 角色描述
	:return:
	'''
	if request.method == 'POST':
		name = request.POST.get('name', None)
		status = request.POST.get('status', 0)
		describe = request.POST.get('describe', None)
		if status:
			status = 1
		if name and describe:
			group_obj = Group.objects.create(name=name, status=status, describe=describe)
			menu_obj = Menu.objects.get(id=1)
			group_obj.menu.add(menu_obj)

			messgs = {'code': 0, 'msg': '添加成功!'}
		else:
			messgs = {'code': 1, 'msg': '添加失败!'}

		return JsonResponse(messgs)

	return render(request, 'itom/group/add.html')

@admin_required
def group_edit(request, id):
	'''
	角色修改，get请求对应id的角色信息，post传递修改数据
	:param request:
	status: 角色状态（0表示禁用，1表示启用）
	describe: 角色描述
	:param id:
	id：角色对应的id
	:return:
	get请求返回渲染html
	post请求返回json
	'''
	if request.method == 'POST':
		status = request.POST.get('status', 0)
		describe = request.POST.get('describe', None)
		if status:
			status = 1
		if status or describe:
			Group.objects.filter(id=id).update(status=status, describe=describe)
			messgs = {'code': 0, 'msg': '修改成功!'}
		else:
			messgs = {'code': 1, 'msg': '修改失败!'}

		return JsonResponse(messgs)

	data = Group.objects.filter(id=id).first()

	return render(request, 'itom/group/edit.html', {"data": data})

@admin_required
def group_auth(request, id):
	if request.method == 'POST':
		tree_val = request.POST.get('tree_val', None)
		if tree_val:
			tlist = [int(i) for i in list(filter(None, tree_val.strip('\'').split('|')))]
			menu_obj = Menu.objects.filter(id__in=tlist)
			group_obj = Group.objects.get(id=id)
			#先清空对应权限
			group_obj.menu.clear()
			#然后添加对应权限
			group_obj.menu.add(*menu_obj)
			messgs = {'code': 0, 'msg': '修改成功!'}
		else:
			messgs = {'code': 1, 'msg': '修改失败!'}
		return JsonResponse(messgs)

	return render(request, 'itom/group/auth.html', {'mid': id})

@admin_required
def group_auth_json(request, id):
	data = Menulist.json_to_menu(int(id))

	return JsonResponse(data, safe=False)

@admin_required
def group_del(request):
	'''
	角色删除
	:param request:
	id: 角色对应的id
	:return:
	post请求返回json
	'''
	if request.method == 'POST':
		id = request.POST.get('id', None)
		if id:
			Group.objects.filter(id=id).delete()
			messgs = {'code': 0, 'msg': '删除成功!'}
		else:
			messgs = {'code': 1, 'msg': '删除失败!'}

		return JsonResponse(messgs)

@admin_required
def user(request):
	'''
	用户管理
	:param request:
	page: 页数
	limit: 每页数据量
	data: 所有post请求参数，包含查询条件(user,name,email,org,group)
	dict: 引进user_search函数处理查询条件，返回dict格式数据
	:return:
	get请求返回渲染html
	post请求返回json
	'''
	if request.method == 'POST':
		page = request.POST.get('page', 1)
		limit = request.POST.get('limit', 10)
		data = request.POST.dict()
		#判断查询条件
		dict = user_serach(data)
		if dict:
			user_list = User.objects.filter(**dict)
		else:
			user_list = User.objects.all()
		paginator = Paginator(user_list, int(limit))
		data = [{"id": n.id, "user": n.user, "name": n.name, "email": n.email,
				 "reg_time": n.reg_time.strftime('%Y-%m-%d %H:%M:%S'), "in_ip": n.in_ip,
				 "up_time": n.up_time.strftime('%Y-%m-%d %H:%M:%S'),
				 "group": Group.objects.get(id=n.group_id).name,
				 "org": Org.objects.get(id=n.org_id).name} for n in paginator.page(int(page)).object_list]
		data = {
			"code": 0,
			"msg": "",
			"count": paginator.count,
			"data": data,
		}
		return JsonResponse(data)
	org = Org.objects.all()
	group = Group.objects.all()

	return render(request, 'itom/user/index.html', {"org": org, "group": group})

@admin_required
def user_add(request):
	'''
	用户添加
	:param request:
	data: 所有post请求参数（包含：user,name,org,group,email）
	:return:
	get: 查询部门和角色信息，通过render函数
	渲染对应html返回给浏览器
	post: 先查询post传递user值数据库是否存
	在，不存在的情况下通过调用Sendmail类随
	机生成8位的密码，查询部门和角色外键信息，
	完成插入数据之后，继续将账号和密码通过
	Sendmail类发送邮件给对应邮箱地址；不论
	是否失败都会返回json格式的状态信息
	'''
	if request.method == 'POST':
		data = request.POST.dict()
		if data:
			utf = User.objects.filter(user=data['user']).first()
			if utf:
				messgs = {'code': 1, 'msg': '账号已经存在!'}
			else:
				#create password
				pwd = Sendmail.pass_random()
				org = Org.objects.get(id=int(data['org']))
				group = Group.objects.get(id=int(data['group']))
				User.objects.create(
					user=data['user'],
					name=data['name'],
					password=pwd,
					org=org,
					group=group,
					email=data['email']
				)
				try:
					#发送邮件
					Sendmail.mail_template(data['user'], pwd)
					Sendmail.send_mail(data['email'])
					messgs = {'code': 0, 'msg': '添加成功!'}
				except:
					messgs = {'code': 1, 'msg': '邮件发送失败!'}
		else:
			messgs = {'code': 1, 'msg': '添加失败!'}
		return JsonResponse(messgs)

	org = Org.objects.all()
	group = Group.objects.all()

	return render(request, 'itom/user/add.html', {"org": org, "group": group})

@admin_required
def user_edit(request, id):
	'''
	用户编辑
	:param request:
	org: 部门id
	group:  角色id
	email: 邮箱地址
	:param id:
	id：用户id
	:return:
	get: 查询对应用户id信息，所有部门、角色信息，
	通过render函数渲染对应html返回给浏览器
	post: 将传递过来的信息，先做下判断，然后再
	进行修改，成功或失败都会返回json格式状态信息
	'''
	if request.method == 'POST':
		org = request.POST.get('org', None)
		group = request.POST.get('group', None)
		email = request.POST.get('email', None)
		if org and group and email:
			org = Org.objects.get(id=int(org))
			group = Group.objects.get(id=int(group))
			User.objects.filter(id=id).update(
				org_id=org,
				group_id=group,
				email=email
			)
			messgs = {'code': 0, 'msg': '修改成功!'}
		else:
			messgs = {'code': 1, 'msg': '修改失败!'}

		return JsonResponse(messgs)

	data = User.objects.filter(id=id).first()
	org = Org.objects.all()
	group = Group.objects.all()
	return render(request, 'itom/user/edit.html', {"data": data, "org": org, "group": group})

@admin_required
def user_reset(request):
	'''
	用户密码重置
	:param request:
	id：用户id
	:return:
	post: 判断传递id信息，先查询用户信息，通过Sendmail类生效新密码，
	利用model里面User中password函数将密码加密，并且更新，然后发送
	新密码给对用邮箱地址，成功或失败都会返回json格式状态信息
	'''
	if request.method == 'POST':
		id = request.POST.get('id', None)
		if id:
			#reset
			user = User.objects.filter(id=id).first()
			pwd = Sendmail.pass_random()
			user.password = pwd
			user.save()
			try:
				Sendmail.mail_template(user.user,pwd)
				Sendmail.send_mail(user.email)
				messgs = {'code': 0, 'msg': '密码重置成功!'}
			except:
				messgs = {'code': 1, 'msg': '邮件发送失败!'}
		else:
			messgs = {'code': 1, 'msg': '密码重置失败!'}

		return JsonResponse(messgs)

@admin_required
def user_del(request):
	'''
	用户删除
	:param request:
	id：用户id
	:return:
	post: 判断传递id信息，通过id删除对应的记录，
	成功或失败都会返回json格式状态信息
	'''
	if request.method == 'POST':
		id = request.POST.get('id', None)
		if id:
			User.objects.filter(id=id).delete()
			messgs = {'code': 0, 'msg': '删除成功!'}
		else:
			messgs = {'code': 1, 'msg': '删除失败!'}

		return JsonResponse(messgs)

@admin_required
def menu(request):
	data = Menulist.mlist_to_tree()
	Menulist.glist_to_tree(data)
	mlist = Menulist.list_to_menu(data)
	list = json.dumps(mlist)

	return render(request, 'itom/menu/index.html', {'list': list})

@admin_required
def menu_add(request):
	if request.method == 'POST':
		name = request.POST.get('name', None)
		fid = request.POST.get('fid', 0)
		hide = request.POST.get('hide', 0)
		url = request.POST.get('url', '')
		sort = request.POST.get('sort', 0)
		icon = request.POST.get('icon', '')
		if hide:
			hide = 1
		if name:
			try:
				Menu.objects.create(
					name=name,
					fid=fid,
					url=url,
					sort=sort,
					icon=icon,
					auth=0,
					hide=hide,
					level=0
				)
				messgs = {'code': 0, 'msg': '添加成功！'}
			except:
				messgs = {'code': 1, 'msg': '添加失败！'}
		else:
			messgs = {'code': 1, 'msg': '添加失败！'}

		return JsonResponse(messgs)

	data = Menulist.mlist_to_tree()
	list = Menulist.form_at_tree(data)
	list.insert(0, {"id": "0", "showName": u"顶级菜单"})
	mlist = [(int(n['id']), n['showName']) for n in list]

	return render(request, 'itom/menu/add.html', {'mlist': mlist})

@admin_required
def menu_edit(request, id):
	if request.method == 'POST':
		name = request.POST.get('name', None)
		fid = request.POST.get('fid', 0)
		hide = request.POST.get('hide', 0)
		url = request.POST.get('url', '')
		sort = request.POST.get('sort', 0)
		icon = request.POST.get('icon', '')
		if hide:
			hide = 1
		if name:
			try:
				Menu.objects.filter(id=id).update(
					name=name,
					fid=fid,
					url=url,
					sort=sort,
					icon=icon,
					hide=hide
				)
				messgs = {'code': 0, 'msg': '修改成功！'}
			except:
				messgs = {'code': 1, 'msg': '修改失败！'}
		else:
			messgs = {'code': 1, 'msg': '修改失败！'}

		return JsonResponse(messgs)

	menu = Menu.objects.get(id=id)
	data = Menulist.mlist_to_tree()
	list = Menulist.form_at_tree(data)
	list.insert(0, {"id": "0", "showName": u"顶级菜单"})
	mlist = [(int(n['id']), n['showName']) for n in list]

	return render(request, 'itom/menu/edit.html', {'menu': menu, 'mlist': mlist})

@admin_required
def menu_del(request):
	if request.method == 'POST':
		id = request.POST.get('id', None)
		if id:
			fid = Menu.objects.filter(fid=int(id)).first()
			if fid:
				messgs = {'code': 1, 'msg': '请先删除子菜单！'}
			else:
				Menu.objects.filter(id=int(id)).delete()
				messgs = {'code': 0, 'msg': '删除成功！'}
		else:
			messgs = {'code': 1, 'msg': '菜单ID为空！'}

		return JsonResponse(messgs)

@method_decorator(login_required, name='dispatch')
class UserInfo(View):

	def get(self, request, id):
		uinfo = User.objects.get(id=id)
		if uinfo:
			data = {
				"user": uinfo.user,
				"name": uinfo.name,
				"org": Org.objects.get(id=uinfo.org_id).name,
				"group": Group.objects.get(id=uinfo.group_id).name,
				"email": uinfo.email,
				"in_ip": uinfo.in_ip,
				"up_time": uinfo.up_time.strftime('%Y-%m-%d %H:%M:%S')
			}
			return render(request, 'itom/user/userinfo.html', {"data": data})

	def post(self, request, id):
		oldpwd = request.POST.get('oldPassword', None)
		pwd = request.POST.get('password', None)
		repwd = request.POST.get('repassword', None)
		if oldpwd and pwd and repwd:
			user = User.objects.get(id=id)
			if user.verify_password(oldpwd):
				if pwd == repwd:
					user.password = pwd
					user.save()
					messgs = {'code': 0, 'msg': '修改成功!'}
				else:
					messgs = {'code': 1, 'msg': '新密码不一致!'}
			else:
				messgs = {'code': 1, 'msg': '老密码错误!'}
		else:
			messgs = {'code': 1, 'msg': '修改密码异常!'}

		return JsonResponse(messgs)

	@staticmethod
	def password(request):
		return render(request, 'itom/user/password.html')

from updatetask.Sendmail import execute

@admin_required
def update_mail(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = Renewmail.objects.filter(dates=keyword)
        else:
            org_list = Renewmail.objects.all()
        paginator = Paginator(org_list, int(limit))
        data = [{"id": n.id, "platform": n.platform, "program": n.program, "group": n.group, "dates": n.dates,
                 "ctime": n.ctime.strftime('%Y-%m-%d %H:%M:%S'), "result": n.result} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)

    return render(request, 'itom/upmail/index.html')

@admin_required
def up_execute(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        program = request.POST.get('program')
        group = request.POST.get('group')
        dates = request.POST.get('date')
        if platform and program and group and dates:
            try:
                result = execute(platform, program, group, dates)
                Renewmail.objects.create(platform=platform, program=program, group=group, dates=dates, result=result)
                messgs = {'code': 0, 'msg': '发送成功!'}
            except:
                messgs = {'code': 1, 'msg': '发送失败!'}
        else:
            messgs = {'code': 1, 'msg': '执行失败!'}

        return JsonResponse(messgs)
    return render(request, 'itom/upmail/add.html')

@admin_required
def async(request):
    if request.method == 'POST':
        page = request.POST.get('page', 1)
        limit = request.POST.get('limit', 10)
        keyword = request.POST.get('keyword', None)
        if keyword:
            org_list = Async.objects.filter(version=keyword)
        else:
            org_list = Async.objects.all()
        paginator = Paginator(org_list, int(limit))
        data = [{"id": n.id, "platform": n.platform, "program": n.program, "week": n.week,"group": n.group,
                 "ctime": n.ctime.strftime('%Y-%m-%d %H:%M:%S'), "result": n.result} for n in paginator.page(int(page)).object_list]
        data = {
            "code": 0,
            "msg": "",
            "count": paginator.count,
            "data": data,
        }
        return JsonResponse(data)

    return render(request, 'itom/async/index.html')

@admin_required
def asyncexecute(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        program = request.POST.get('program')
        version = request.POST.get('version')
        week = request.POST.get('week')
        group = request.POST.get('group')
        ftpadd = request.POST.get('ftpadd')
        if platform and program and version and week and group and ftpadd:
            try:
                pro_info = {
                    'platform': platform,
                    'program': program,
                    'version': version,
                    'week': week,
                    'group': group,
                    'ftpadd': ftpadd,
                    'user': 'salt',
                    'pwd': 'saltstack'
                }
                headers = {'content-type': 'application/json'}
                r = requests.post("http://192.168.5.105:8002/json", data=json.dumps(pro_info), headers=headers)
                print(r.json())
                # result = execute(platform, program, group, week)
                # Renewmail.objects.create(platform=platform, program=program, group=group, dates=week, result=result)
                messgs = {'code': 0, 'msg': '发送成功!'}
            except:
                messgs = {'code': 1, 'msg': '发送失败!'}
        else:
            messgs = {'code': 1, 'msg': '执行失败!'}

        return JsonResponse(messgs)
    return render(request, 'itom/async/add.html')

