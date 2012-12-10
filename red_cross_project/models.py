#models.py: this is the global models for the whole system
#author: SIQI
from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
	title = models.CharField(max_length=50)
	update_time = models.DateTimeField()
	post_time = models.DateTimeField()
	stamps = models.ManyToManyField(Stamp, null=True , related_name = 'Threads')

class Stamp(models.Model):
	name = models.CharField(max_length=15)

class UserStatics(models.Model):
	thanks_amount = models.IntegerField(default=0)
	post_amount = models.IntegerField(default=0)
	reply_amount = models.IntegerField(default=0)
	question_amount = models.IntegerField(default=0)
	answser_amount = models.IntegerField(default=0)
	user = models.ForeignKey(User)

class Profile(models.Model):
	age = models.IntegerField(null=True)		
	gender = models.CharField(default='F',max_length=1)
	enrolled = models.BooleanField(default=False, null=True)
	profile_img = models.ImageField()
	user = ForeignKey(User)


