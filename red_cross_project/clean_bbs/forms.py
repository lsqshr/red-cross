#coding=utf-8

from django import forms 
from red_cross_project.clean_bbs.models import Question,Answer,TempProfile

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('title','content',)
		widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

#not being used currently
class FilterForm(forms.Form):
    time_choices = (('all','全部'),((),()))
    time = forms.ChoiceField()

class TempProfileForm(forms.ModelForm):
    class Meta:
        model = TempProfile
        exclude = ('question')
