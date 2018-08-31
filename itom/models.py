from django.db import models
import django.utils.timezone as timezone
import hashlib, datetime

# Create your models here.

class User(models.Model):
	user = models.CharField(max_length=20, verbose_name="账号")
	name = models.CharField(max_length=20, verbose_name="姓名")
	password_hash = models.CharField(max_length=50, verbose_name="密码")
	email = models.EmailField(verbose_name="邮箱")
	org = models.ForeignKey("Org", on_delete=models.CASCADE, verbose_name="部门")
	group = models.ForeignKey("Group", on_delete=models.CASCADE, verbose_name="组")
	#reg_time = models.IntegerField(verbose_name="注册时间")
	reg_time = models.DateTimeField(default=timezone.now, verbose_name="注册时间")
	in_ip = models.CharField(max_length=20, null=True, verbose_name="登陆IP")
	#up_time = models.IntegerField(blank=True, verbose_name="登陆时间")
	up_time = models.DateTimeField(default=timezone.now, verbose_name="更新时间")

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		pwd = hashlib.md5()
		pwd.update(password.encode(encoding='utf-8'))
		self.password_hash = pwd.hexdigest()

	def verify_password(self, password):
		pwd = hashlib.md5()
		pwd.update(password.encode(encoding='utf-8'))
		if self.password_hash == pwd.hexdigest():
			return True
		else:
			return False


class Org(models.Model):
	name = models.CharField(max_length=20, verbose_name="部门名称")
	describe = models.CharField(max_length=50, verbose_name="部门描述")

	def __str__(self):
		return self.name

class Group(models.Model):
	name = models.CharField(max_length=20, verbose_name="组名称")
	status = models.IntegerField(verbose_name="状态")
	menu = models.ManyToManyField(to="Menu", blank=True, verbose_name="所具有的权限")
	describe = models.CharField(max_length=50, verbose_name="组描述")

	def __str__(self):
		return self.name

class Menu(models.Model):
	name = models.CharField(max_length=20, verbose_name="菜单名称")
	fid = models.IntegerField(verbose_name="fid")
	url = models.CharField(max_length=50, null=True, verbose_name="url")
	auth = models.SmallIntegerField(verbose_name="认证id")
	sort = models.IntegerField(verbose_name="排序id")
	hide = models.SmallIntegerField(verbose_name="是否隐藏")
	icon = models.CharField(max_length=50, null=True, verbose_name="图标")
	level = models.SmallIntegerField(verbose_name="level")

class Renewmail(models.Model):
	id = models.AutoField(primary_key=True)
	platform = models.CharField(max_length=32)
	program = models.CharField(max_length=32)
	group = models.CharField(max_length=32)
	dates = models.DateField(null=True)
	ctime = models.DateTimeField(auto_now_add=True)
	result = models.CharField(max_length=64)

	def __str__(self):
		return self.result
