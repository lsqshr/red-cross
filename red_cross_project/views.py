#coding=utf-8

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

import account.views

from .forms import SignupForm
from red_cross_project.forms import ProfileForm
from red_cross_project.models import ExtraProfile
from red_cross_project.settings import MEDIA_ROOT

import datetime
import os

class SignupView(account.views.SignupView):
    
    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    
    def create_profile(self, form):
        profile = self.created_user.profile
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.save()
        ex_profile = ExtraProfile(register_time=datetime.datetime.now(),user=self.created_user)
        ex_profile.save()

@login_required
def profile_settings(request, **kwargs):

	context = {}
	if hasattr(request.user,'user_profile'): 
		ex_profile = request.user.user_profile
	else:
		ex_profile = ExtraProfile()
		ex_profile.user = request.user
		ex_profile.save()

	if request.method == 'POST':
		if 'save' in request.POST:
			form = ProfileForm(request.POST,request.FILES)
			if form.is_valid():
				profile = form.save(commit=False)
				#find user's previously stored profile info and overwrite it
				ex_profile.gender = profile.gender
				ex_profile.age = profile.age
				ex_profile.enrolled = profile.enrolled
				if profile.profile_img:
					#if the user uploads a new profile image
					#if the user has set a profile image before
					#find the previous one's path and delete it from the file-system(if file exist)
					if ex_profile.profile_img:
						path = os.path.join(MEDIA_ROOT,ex_profile.profile_img.name)
						if os.path.exists(path) :
							os.remove(path)
					ex_profile.profile_img = profile.profile_img
				ex_profile.save()

				context['message'] = '您的个人信息已经被成功更新' 
			else:
				context['message'] = '对不起,由于格式问题您的信息没有被成功更新'
			context['form'] = form
	else:
		form = ProfileForm(instance = ex_profile)
		context['form'] = form

	return render_to_response('edit_profile.html', context, \
		context_instance=RequestContext(request, {}) )
