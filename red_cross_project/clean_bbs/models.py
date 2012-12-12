from django.db import models
from red_cross_project.models import Thread

# Create your models here.
class Question(Thread):
	content = models.CharField(max_length = 2000)
	
	def __unicode__(self):	
		return self.title
		
	class Meta:
		ordering = ['-update_time']

class Answer(Thread):
	question = models.ForeignKey(Question,related_name = 'answers')
	thanks = models.IntegerField(default = 0)
	disagree = models.IntegerField(default = 0)
	content = models.CharField(max_length = 10000)