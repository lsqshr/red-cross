#coding=utf-8

from django.template.context import RequestContext
from django.shortcuts import render_to_response

import account.views

from .forms import SignupForm
from red_cross_project.forms import ProfileForm


class SignupView(account.views.SignupView):
    
    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    
    def create_profile(self, form):
        profile = self.created_user.profile
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.save()

def profile_settings(request, **kwargs):

	context = {}

	if request.method == 'POST':
		if 'save' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				form.save(commit=False)
				context['message'] = '您的个人信息已经被成功更新' 
			else:
				context['message'] = '对不起,由于格式问题您的信息没有被成功更新'
			context['form'] = form
			return render_to_response('edit_profile.html', context, \
				context_instance=RequestContext(request, {}) )
	else:
		context['form'] = ProfileForm()
		return render_to_response('edit_profile.html', context, \
			context_instance=RequestContext(request, {}) )


