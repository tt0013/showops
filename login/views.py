from django.shortcuts import render, redirect, render_to_response
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
import random, hashlib, datetime
from itom.models import User, Org, Group
from public.views import Menulist
# Create your views here.


class Login(View):

	def get(self, request):
		if request.session.get('is_login', None) == 1:
			return redirect('/itom/')
		return render(request, 'login/login.html')

	def post(self, request):
		challenge = request.POST.get('geetest_challenge', None)
		validate = request.POST.get('geetest_validate', None)
		user = request.POST.get('user', None)
		pwd = request.POST.get('password', None)
		m = hashlib.md5()
		if not challenge:
			messages.error(request, '请输入验证码！', extra_tags='danger')
		else:
			#md5
			m.update(challenge.encode("utf-8"))
			if m.hexdigest() == validate:
				uinfo = User.objects.filter(user=user).first()
				if uinfo is not None and uinfo.verify_password(pwd):
					#获取用IP
					uinfo.in_ip = self.get_ip(request)
					#生成用户登陆时间
					uinfo.up_time = datetime.datetime.now()
					#更新数据
					uinfo.save()
					#session
					request.session['uid'] = uinfo.id
					request.session['username'] = uinfo.name
					request.session['is_login'] = 1
					#生成菜单
					menulist = Menulist.condition_to_tree(uinfo.id)
					mdict = Menulist.form_at_tree(menulist)
					request.session['enable_url'] = list(filter(None, list(set(auth['url'] for auth in mdict))))
					return redirect('/itom/')
				else:
					messages.error(request, '用户或密码错误！', extra_tags='danger')
					return render(request, 'login/login.html')
			else:
				messages.error(request, '验证码错误！', extra_tags='danger')
				return render(request, 'login/login.html')





	#获取用户真实IP
	def get_ip(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
		else:
			ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
		return ip

def Verification(request):
	'''
	生成验证码
	:param request:
	:return:
	'''
	gt_captcha_id = '9d80bd1e6eed71d51a760ade1ee54e51'
	m = hashlib.md5()
	m.update(str(random.randint(0, 100)).encode("utf-8"))
	rnd1 = m.hexdigest()
	m.update(str(random.randint(0, 100)).encode("utf-8"))
	rnd2 = m.hexdigest()
	challenge = rnd1 + rnd2[0:2]
	result = {
		'success': 0,
		'gt': gt_captcha_id,
		'challenge': challenge,
		'new_captcha': 1
	}
	return JsonResponse(result)

def logout(request):
	request.session.clear()
	messages.success(request, '后台退出成功！', extra_tags='success')
	return redirect('/auth/login/')

def page_not_found(request):
	'''
	定义404页面
	:param request:
	:return:
	'''
	return render_to_response('error/404.html')


def page_error(request):
	'''
	定义500错误页面
	:param request:
	:return:
	'''
	return render_to_response('error/500.html')


def permission_denied(request):
	'''
	定义403页面
	:param request:
	:return:
	'''
	return render_to_response('error/403.html')