from django.shortcuts import render
import os, re, json
import smtplib
from random import Random
from functools import wraps
from email.header import Header
from email.mime.text import MIMEText
from .apps import PublicConfig as pconfig
from django.shortcuts import render, redirect, HttpResponse
from itom.models import Menu, Group
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Sendmail:
	'''
	生成新密码，将账号和密码发送对用的邮箱地址
	'''
	@staticmethod
	def pass_random(randomlength=8):
		passwd = ''
		chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
		length = len(chars) - 1
		random = Random()
		for i in range(randomlength):
			passwd += chars[random.randint(0, length)]

		return passwd

	@staticmethod
	def mail_template(uemail,passwd):
		with open(r''+os.path.join(BASE_DIR, "public", "tmp", "usermail.html")+'', 'r', encoding='UTF-8') as oldf:
			oldf = oldf.readlines()
			with open(r''+os.path.join(BASE_DIR, "public", "tmp", 'news.html')+'','w+', encoding='UTF-8') as newsf:
				for f in oldf:
					news = f.strip('\n')
					ere = re.findall(r'u-email',news)
					if ere:
						news = re.sub(r'u-email', uemail, news)
					pre = re.findall(r'password',news)
					if pre:
						news = re.sub(r'password', passwd, news)
					ure = re.findall(r'Backstageurl',news)
					if ure:
						news = re.sub(r'Backstageurl', pconfig.Mail['adminurl'], news)
					newsf.write(news+'\n')

	@staticmethod
	def send_mail(sendmail):
		# html
		html = open(r''+os.path.join(BASE_DIR, "public", "tmp", 'news.html')+'', 'r', encoding='UTF-8').read()
		msg = MIMEText(html, 'html', 'utf-8')

		sub = '运维后台账号'
		Me = pconfig.Mail['user']
		msg['Subject'] = Header(sub, 'utf-8')
		msg['From'] = Me
		sendmaillist = sendmail.split(",")
		msg['To'] = ";".join(sendmaillist)

		#msg.attach(html_part)

		# send mail
		try:
			s = smtplib.SMTP()
			s.connect(pconfig.Mail['host'])
			s.login(pconfig.Mail['user'], pconfig.Mail['pswd'])
			s.sendmail(Me, sendmaillist, msg.as_string())
			s.close()
			return True
		except Exception as e:
			print(str(e))
			return False

def user_serach(data):
	'''
	分析用户管理查询条件，将处理完的结果以字典格式返回
	:param dict:
	:return:
	'''
	dict = {}
	for i in data:
		if i == 'page' or i == 'limit':
			continue
		if not data[i] == '':
			dict[i] = data[i]

	return dict

class Menulist:

	@staticmethod
	def mlist_to_tree():
		'''
		生成菜单列表
		:param gid:
		:return:
		'''
		tree = {}
		tid = 0
		data = Menu.objects.order_by('id').all()
		if data:
			refer = {}
			for i in data:
				refer[i.id] = {
					"id": '%s' % str(i.id),
					"name": i.name,
					"fid": '%s' % str(i.fid),
					"url": i.url,
					"login": '%s' % str(i.auth),
					"sort": '%s' % str(i.sort),
					"hide": '%s' % str(i.hide),
					"icon": i.icon,
					"level": '%s' % str(i.level)
				}

			for i in data:
				parentId = i.fid
				if parentId == 0:
					tree[tid] = refer[i.id]
					tid += 1
				else:
					if parentId in refer:
						if '_child' not in refer[parentId]:
							num = 0
							refer[parentId]['_child'] = {}
						else:
							num = len(refer[parentId]['_child'])
						refer[parentId]['_child'][num] = refer[i.id]

		return tree

	@staticmethod
	def condition_to_tree(id):
		'''
		根据条件生成菜单列表
		:param gid:
		:return:
		'''
		tree = {}
		tid = 0
		menu_obj = Menu.objects.order_by('id').all()
		if int(id) != 1:
			group_obj = Group.objects.get(id=id)
			glist = group_obj.menu.all()

			data = []
			for m in menu_obj:
				for g in glist:
					if int(m.id) == int(g.id):
						data.append(m)
					else:
						continue
		else:
			data = menu_obj
		if data:
			refer = {}
			for i in data:
				if int(i.hide) == 1:continue
				refer[i.id] = {
					"id": '%s' % str(i.id),
					"name": i.name,
					"fid": '%s' % str(i.fid),
					"url": i.url,
					"auth": '%s' % str(i.auth),
					"sort": '%s' % str(i.sort),
					"hide": '%s' % str(i.hide),
					"icon": i.icon,
					"level": '%s' % str(i.level)
				}
				refer[i.id]

			for i in data:
				if int(i.hide) == 1:continue
				parentId = i.fid
				if parentId == 0:
					tree[tid] = refer[i.id]
					tid += 1
				else:
					if parentId in refer:
						if '_child' not in refer[parentId]:
							num = 0
							refer[parentId]['_child'] = {}
						else:
							num = len(refer[parentId]['_child'])
						refer[parentId]['_child'][num] = refer[i.id]

		return tree

	@staticmethod
	def list_to_menu(data):
		'''

		:param data:
		:return:
		'''
		mlist = []
		for i in data:
			if '_child' not in data[i]:
				mlist.append(data[i])
			else:
				child = data[i]['_child']
				data[i].pop('_child')
				data[i]['children'] = Menulist.list_to_menu(child)
				mlist.append(data[i])

		return mlist

	@staticmethod
	def glist_to_tree(tree):
		strtree = ''
		for t in tree:
			if int(tree[t]['fid']) == 0 and int(tree[t]['id']) == 1:
				strtree = '''
				<li data-name="{}" class="layui-nav-item">
				<a href="javascript:;" lay-href="{}" lay-tips="{}" lay-direction="2" class="layui-this">
				<i class="layui-icon {}"></i>
				<cite>{}</cite>
				</a>
				</li>
				'''.format('ops'+str(tree[t]['id']), tree[t]['url'], tree[t]['name'], tree[t]['icon'], tree[t]['name'])
			else:
				if int(tree[t]['fid']) == 0:
					strtree += '''
					<li data-name="{}" class="layui-nav-item">
					<a href="javascript:;" lay-tips="{}" lay-direction="2">
					<i class="layui-icon {}"></i>
					<cite>{}</cite>
					</a>
					'''.format('ops'+str(tree[t]['id']), tree[t]['name'], tree[t]['icon'], tree[t]['name'])
					if '_child' in tree[t]:
						strtree += '''
						<dl class="layui-nav-child">
						'''
						for c in tree[t]['_child']:
							strtree += '''
							<dd data-name="console">
							<a lay-href="{}">{}</a>
							</dd>
							'''.format(tree[t]['_child'][c]['url'], tree[t]['_child'][c]['name'])
						strtree += '''</dl>'''
					strtree += '''</li>'''
		return strtree

	@staticmethod
	def form_at_tree(data, lv=0):
		formattree = []
		for i in data:
			title_prefix = ''
			for n in range(0, lv):
				title_prefix += "|---"

			data[i]['lv'] = lv
			if lv == 0:
				data[i]['namePrefix'] = ''
				data[i]['showName'] = data[i]['name']
			else:
				data[i]['namePrefix'] = title_prefix
				data[i]['showName'] = title_prefix + data[i]['name']
			if '_child' not in data[i]:
				formattree.append(data[i])
			else:
				child = data[i]['_child']
				del data[i]['_child']
				formattree.append(data[i])
				middle = Menulist.form_at_tree(child, lv + 1)
				formattree = formattree + middle

		return formattree

	@staticmethod
	def json_to_menu(id):
		menu_obj = Menu.objects.order_by('id').all()
		group_obj = Group.objects.get(id=id)
		mlist = group_obj.menu.all()

		data = []
		if mlist:
			for m in menu_obj:
				action = 0
				for g in mlist:
					if m.id == g.id:
						action = 1
				if action == 1:
					data.append({"id": m.id, "name": m.name, "pId": m.fid, "url": m.url, "checked": "true"})
				else:
					data.append({"id": m.id, "name": m.name, "pId": m.fid, "url": m.url})
		else:
			for m in menu_obj:
				data.append({"id": m.id, "name": m.name, "pId": m.fid, "url": m.url})

		return data

def login_required(func):
	@wraps(func)
	def inner(request, *args, **kwargs):
		is_login = request.session.get('is_login', None)
		if is_login != 1:
			return redirect('/auth/login/')

		return func(request, *args, **kwargs)

	return inner

def admin_required(func):
	@wraps(func)
	def decorated_view(request, *args, **kwargs):
		uid = request.session.get('uid', None)
		if uid != 1:
			auth_url = request.session.get('enable_url')
			if not auth_url:
				return redirect('/auth/login/')
			if request.path not in auth_url:
				return HttpResponse(status=403)
		return func(request, *args, **kwargs)

	return decorated_view
