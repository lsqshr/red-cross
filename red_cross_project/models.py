#coding=utf-8
#models.py: this is the global models for the whole system
#author: SIQI
from django.db import models
from django.contrib.auth.models import User
import cloudinary.models
import datetime

class MyCloudinaryField(cloudinary.models.CloudinaryField):
    def upload_options(self, model_instance):
       return {'public_id': model_instance.user.id}

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
	#profile_img = models.ImageField(upload_to = 'images/%Y/%m/%d', null=True)
	#heroku does not work for file uploading so I imported one addon called cloudinary.
	profile_img = MyCloudinaryField('image',null=True) 
	role = models.CharField(default='P',max_length=1,choices=role_choices) #P:patient/D:doctor, it can only changed by administrator
	position = models.CharField(default='医师',max_length=10,null=True)

	def __unicode__(self):
		return self.user.username

