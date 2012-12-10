from django.db import models
from red_cross_project.models import Thread

# Create your models here.
class Question(Thread):
	content = models.CharField(max_length = 2000)

class Answer(Thread):
	question = models.ForeignKey(Question,related_name = 'Answers')
	thanks = models.IntegerField()
	disagree = models.IntegerField()
	content = models.CharField(max_length = 10000)