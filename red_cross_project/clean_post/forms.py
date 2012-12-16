#coding=utf-8

from django import forms 
from red_cross_project.clean_post.models import Post, Reply 

class PostForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields = ('title','content',)
		widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply 
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }