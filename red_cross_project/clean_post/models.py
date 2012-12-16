from django.db import models
from red_cross_project.models import Thread

# Create your models here.
class Post(Thread):
	thanks = models.IntegerField(default = 0)
	diagree = models.IntegerField(default = 0)
	content = models.CharField(max_length = 10000)

class Reply(Thread):
	post = models.ForeignKey(Post,related_name = 'Replies')
	content = models.CharField(max_length = 240)
