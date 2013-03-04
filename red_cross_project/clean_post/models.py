#coding=utf8
from django.db import models
from red_cross_project.models import Thread

# Create your models here.
class Post(Thread):
	thanks = models.IntegerField(default = 0)
	diagree = models.IntegerField(default = 0)
	content = models.CharField(max_length = 32767, verbose_name = "内容")

	def __unicode__(self):
		return self.title + u" | 作者:" + self.author.username + " | id:" + str(self.id)

	class Meta:
		verbose_name = "健康贴士"

class Reply(Thread):
	post = models.ForeignKey(Post,related_name = 'Replies', verbose_name="对应的健康贴士")
	content = models.CharField(max_length = 240, verbose_name="内容")

	def __unicode__(self):
		return self.title + u" | 作者:" + self.author.username + " | id:" + str(self.id)

	class Meta:
		verbose_name = "回答"
