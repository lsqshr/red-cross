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

class Answer(Thread):
	question = models.ForeignKey(Question,related_name = 'answers')
	thanks = models.IntegerField(default = 0)
	disagree = models.IntegerField(default = 0)
	content = models.CharField(max_length = 10000)

class TempProfile(models.Model):
	GENDER_CHOICES = (('M','Male'),('F','Female'),)
	question = models.ForeignKey(Question, related_name = 'temp_profile')
	age = models.IntegerField(default = 0)
	gender = models.CharField(max_length = 1, choices = GENDER_CHOICES , default = 'F')
	enrolled = models.BooleanField(default = True)
	history = models.CharField(max_length = 255, null = True) # history of the diseases the user has suffered before