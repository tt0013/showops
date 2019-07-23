from django.db import models

# Create your models here.

class SinaShow_Bandwidth(models.Model):
    id = models.AutoField(primary_key=True)
    Time = models.IntegerField()
    Week = models.CharField(max_length=15)
    SHOW_JIAXING = models.IntegerField()
    SHOW_NingBo = models.IntegerField()
    SHOW_BaoJi = models.IntegerField()
    SHOW_KS = models.IntegerField()
    SHOW_HangZhou = models.IntegerField()
    SHOW_GanSu = models.IntegerField()
    SHOW_HG = models.IntegerField()
    SHOW_ZhengZhou = models.IntegerField()
    SHOW_JinHua = models.IntegerField()
    SHOW_ChangChun = models.IntegerField()
    SHOW_ChangZhi = models.IntegerField()
    SHOW_JinHua1 = models.IntegerField()
    SHOW_JiaXing1 = models.IntegerField()
    Total = models.IntegerField()

class SinaShow_MaxUserTraffic(models.Model):
    id = models.AutoField(primary_key=True)
    Time = models.IntegerField()
    Week =  models.CharField(max_length=15)
    morn_useridnum = models.IntegerField()
    morn_traffic = models.IntegerField()
    after_useridnum = models.IntegerField()
    after_traffic = models.IntegerField()
    morn_time = models.CharField(max_length=25)
    after_time = models.CharField(max_length=25)

class SinaShow_AvsUser(models.Model):
    id = models.AutoField(primary_key=True)
    Time = models.IntegerField()
    PointTime = models.CharField(max_length=25)
    Week =  models.CharField(max_length=25)
    Avs_Big_Num = models.IntegerField()
    Avs_Over_Num = models.IntegerField()
    Avs_General_Num = models.IntegerField()
    Mic_Big_Num = models.IntegerField()
    Mic_Over_Num = models.IntegerField()
    Mic_General_Num = models.IntegerField()
    Mic_Vip_Num = models.IntegerField()
    Traffic = models.IntegerField()

class Fengbo_Bandwidth(models.Model):
    id = models.AutoField(primary_key=True)
    Dtime = models.BigIntegerField(null=False)
    Week = models.CharField(max_length=32, null=False)
    Usernum = models.IntegerField(null=False)
    Anchornum = models.IntegerField(null=False)
    Wangsunum = models.IntegerField(null=True)
    Audionum = models.IntegerField(null=False)
    Videonum = models.IntegerField(null=False)
    Upbindwidth = models.IntegerField(null=False)
    Downbindwidth = models.IntegerField(null=False)

class YiShow_Bandwidth(models.Model):
    id = models.AutoField(primary_key=True)
    Dtime = models.BigIntegerField()
    Week = models.CharField(max_length=32)
    Motorinwidth = models.FloatField(null=False)
    Motoroutwidth = models.FloatField(null=False)
    Bgpinwidth = models.FloatField(null=False)
    Bgpoutwidth = models.FloatField(null=False)
    Buzznum = models.IntegerField(null=False)
    Cdnwidth = models.IntegerField(null=False)




