#coding=utf8
from django.db import models
from red_cross_project.models import Thread

# Create your models here.
class Question(Thread):
	content = models.CharField(max_length = 2000)
	
	def sorted_answers(self):
		return self.answers.order_by('author__user_profile__role',
                                '-post_time')

	def __unicode__(self):	
		return self.title
		
	class Meta:
		ordering = ['-update_time']
		verbose_name = "问题"

class Answer(Thread):
	question = models.ForeignKey(Question,related_name = 'answers')
	thanks = models.IntegerField(default = 0)
	disagree = models.IntegerField(default = 0)
	content = models.CharField(max_length = 10000)

	class Meta:
		verbose_name = "回答"

class TempProfile(models.Model):
	GENDER_CHOICES = (('M','男'),('F','女'),)
	question = models.ForeignKey(Question, related_name = 'temp_profile', verbose_name="对应的问题")
	age = models.IntegerField(default = 0, verbose_name="年龄")
	gender = models.CharField(max_length = 1, choices = GENDER_CHOICES , default = 'F', verbose_name="性别")
	enrolled = models.BooleanField(default = True, verbose_name="已经是中心病人")
	history = models.CharField(max_length = 255, null = True,verbose_name="已经是中心病人") # history of the diseases the user has suffered before
  
	def __unicode__(self):
		return self.question.title + u" 提问者信息"

	class Meta:
		verbose_name = "访客临时个人信息"