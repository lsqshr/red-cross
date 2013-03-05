#coding=utf-8

from django.template.context import RequestContext
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.files.storage import default_storage

import account.views

from .forms import SignupForm
from red_cross_project.forms import ProfileForm,LoginForm
from red_cross_project.models import ExtraProfile,Staff
#from red_cross_project.settings import MEDIA_ROOT

import datetime
import os

class SignupView(account.views.SignupView):
    
    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    
    def create_profile(self, form):
        profile = self.created_user.profile
        profile.save()
        ex_profile = ExtraProfile(register_time=datetime.datetime.now(),user=self.created_user)
        ex_profile.save()

def homepage(request):
	return render_to_response('homepage2.html',{'page_name':'homepage'},\
		context_instance=RequestContext(request,{}))

def login(request):
	errors=[]
	if request.method == "POST":
		if 'login_submit' in request.POST : #user submited the form to login
			form = LoginForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				username=cd['username']
				password=cd['password']
				user=auth.authenticate(username=username,password=password)
				if user is not None and user.is_active:
				    #Correct Password, and User is marked "active"
				    auth.login(request, user)
				    #Redirect to a success page.
				    return HttpResponseRedirect("/") 
				else:
				    errors.append('用户名或者密码有误')
				    return render_to_response('login.html',{'form':form,\
				                                            'page_name':'Log-in','errors':errors},\
				                                            context_instance=RequestContext(request,{}))
			else:# form is not valid
				errors.append('请提供格式正确的用户名或者密码')
				return render_to_response('login.html',{'form':form,\
				                                        'page_name':'Log-in','errors':errors},\
				                                        context_instance=RequestContext(request,{}))
	else:
		form = LoginForm()
	return render_to_response('login.html', {'form':form,'page_name':'Log-in'},\
	     context_instance=RequestContext(request, {}))

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
				ex_profile.history = profile.history
				if profile.profile_img:
					#if the user uploads a new profile image
					#if the user has set a profile image before
					#find the previous one's path and delete it from the file-system(if file exist)
					if ex_profile.profile_img:
						name = ex_profile.profile_img.name
						if default_storage.exists(name):
							default_storage.delete(name)
						else:
							raise Exception('the previous file path is wrong')
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


def guide(request):
	context = {'page_name': 'guide'}
	return render_to_response('guide.html',context,\
			context_instance=RequestContext(request, {}) )

def staffs(request):
	#get all the staff
	staffs = Staff.objects.all().order_by('rank')
	context = {'staffs':staffs,}
	return render_to_response('staff.html',context,\
			context_instance=RequestContext(request,{}))	