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
	author = models.ForeignKey(User,related_name = 'threads')

class UserStatics(models.Model):
	thanks_amount = models.IntegerField(default=0)
	post_amount = models.IntegerField(default=0)
	reply_amount = models.IntegerField(default=0)
	question_amount = models.IntegerField(default=0)
	answser_amount = models.IntegerField(default=0)
	user = models.ForeignKey(User)


class ExtraProfile(models.Model):

	def upload_to(instance, filename):
	    return 'images'

	gender_choices = (('F','女'),('M','男'),)
	role_choices = (('D','医生'),('P','患者'),)

	age = models.IntegerField(null=True)		
	gender = models.CharField(default='F',max_length=1, choices=gender_choices)
	enrolled = models.NullBooleanField(default=False)
	profile_img = models.ImageField(upload_to = upload_to, null=True)
	register_time = models.DateTimeField(default=datetime.datetime.now())
	user = models.OneToOneField(User, related_name = 'user_profile')
	role = models.CharField(default='P',max_length=1,choices=role_choices) #P:patient/D:doctor, it can only changed by administrator
	position = models.CharField(default='医师',max_length=10,null=True)
