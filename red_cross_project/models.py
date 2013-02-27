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
	'''
	def upload_to(instance, filename):

		if instance.user:
			return os.path.join('images',instance.user.username)
		return 'images/'
	'''
	gender_choices = (('F','女'),('M','男'),)
	role_choices = (('D','医生'),('P','患者'),)

	age = models.IntegerField(null=True)		
	gender = models.CharField(default='F',max_length=1, choices=gender_choices)
	enrolled = models.NullBooleanField(default=False)
	register_time = models.DateTimeField(default=datetime.datetime.now())
	user = models.OneToOneField(User, related_name = 'user_profile')
	profile_img = models.ImageField(upload_to = 'images/%Y/%m/%d', null=True)
	role = models.CharField(default='P',max_length=1,choices=role_choices) #P:patient/D:doctor, it can only changed by administrator

	def __unicode__(self):
		return self.user.username

class Field(models.Model):
	'''
	This is a model class to name a specialized field for Staff class, 
	just avoiding repeating typing the same field names
	'''
	name = models.CharField( max_length = 16 )


	def __unicode__(self):
		return self.name


class Staff(models.Model):
	'''
	this is a model class for displaying the staff info on 'staff page', 
	all the basic stuff of staffs is stored in the ExtraProfile class
	'''
	user = models.OneToOneField(User, related_name = 'staff_profile')
	real_name = models.CharField( max_length = 16 )
	position = models.CharField( max_length = 16 )
	resume = models.CharField( max_length = 1024 )
	rank = models.IntegerField()
	fields = models.ManyToManyField( Field, null=True )

	def __unicode__(self):
		if self.real_name:
			return self.real_name
		else:
			return self.user.username


