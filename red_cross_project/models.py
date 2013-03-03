#coding=utf-8
#models.py: this is the global models for the whole system
#author: SIQI

from django.db import models
from django.contrib.auth.models import User
import datetime

class Stamp(models.Model):
	name = models.CharField(max_length=15)

class Thread(models.Model):
	title = models.CharField(max_length=50)
	update_time = models.DateTimeField(default=datetime.datetime.now())
	post_time = models.DateTimeField(default=datetime.datetime.now())
	stamps = models.ManyToManyField(Stamp, null=True , related_name = 'Threads')
	author = models.ForeignKey(User,related_name = 'threads', null=True)

class UserStatics(models.Model):
	thanks_amount = models.IntegerField(default=0)
	post_amount = models.IntegerField(default=0)
	reply_amount = models.IntegerField(default=0)
	question_amount = models.IntegerField(default=0)
	answser_amount = models.IntegerField(default=0)
	user = models.ForeignKey(User)


class ExtraProfile(models.Model):
	gender_choices = (('F','女'),('M','男'),)
	role_choices = (('D','医生'),('P','患者'),)

	age = models.IntegerField(null=True,verbose_name="年龄")		
	gender = models.CharField(default='F',max_length=1, choices=gender_choices, verbose_name="性别")
	enrolled = models.NullBooleanField(default=False, verbose_name="已经是中心病人")
	register_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="注册时间")
	user = models.OneToOneField(User, related_name = 'user_profile', verbose_name="对应的用户")
	profile_img = models.ImageField(upload_to = 'images/%Y/%m/%d', null=True, verbose_name="肖像照片")
	role = models.CharField(default='P',max_length=1,choices=role_choices, verbose_name="身份") #P:patient/D:doctor, it can only changed by administrator

	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name = "用户个人信息"

class Field(models.Model):
	'''
	This is a model class to name a specialized field for Staff class, 
	just avoiding repeating typing the same field names
	'''
	name = models.CharField( max_length = 16 , verbose_name="名字")

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = "领域"


class Staff(models.Model):
	'''
	this is a model class for displaying the staff info on 'staff page', 
	all the basic stuff of staffs is stored in the ExtraProfile class
	'''
	user = models.OneToOneField(User, related_name = 'staff_profile',verbose_name="员工" )
	real_name = models.CharField( max_length = 16 , verbose_name="真实姓名")
	position = models.CharField( max_length = 16 , verbose_name="职位")
	resume = models.CharField( max_length = 1024, verbose_name="简历" )
	rank = models.IntegerField(verbose_name="排位")#this will effect the appearing order on the staff page
	fields = models.ManyToManyField( Field, null=True , verbose_name="领域")

	def __unicode__(self):
		if self.real_name:
			return self.real_name
		else:
			return self.user.username

	class Meta:
		verbose_name = "员工"

