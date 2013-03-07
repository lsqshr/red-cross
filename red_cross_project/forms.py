#coding=utf8
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

from red_cross_project.models import ExtraProfile
from red_cross_project.profiles.models import Profile

import account.forms


class LoginForm(forms.Form):
	username = forms.CharField( max_length=255,required=True)
	password = forms.CharField( max_length=255,required=True,widget=forms.PasswordInput)

class SignupForm(forms.Form):
	username = forms.CharField( max_length=255,required=True)
	password = forms.CharField( max_length=255,required=True,widget=forms.PasswordInput)
	confirm_password = forms.CharField( max_length=255,required=True,widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("对不起，这个用户名已经有其他人用了")

		return username

	def clean_password(self):
		password = self.cleaned_data['password']
		if len(password) == 0:
			raise forms.ValidationError("密码不能为空")


		return password

class SearchForm(forms.Form):
    key_words = forms.CharField(max_length = 50, required = True)


class ProfileForm(forms.ModelForm):

	class Meta:
		model = ExtraProfile
		exclude = ('role', 'register_time','user','position')
		widget = {
			'profile_img':forms.FileInput,
		}

	def __init__(self,*args,**kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['profile_img'].required = False

