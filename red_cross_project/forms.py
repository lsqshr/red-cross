from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User

from red_cross_project.models import ExtraProfile
from red_cross_project.profiles.models import Profile
import cloudinary.forms
import account.forms


class LoginForm(forms.Form):
	username = forms.CharField( max_length=255,required=True)
	password = forms.CharField( max_length=255,required=True,widget=forms.PasswordInput)

class SignupForm(account.forms.SignupForm):
	pass

class SearchForm(forms.Form):
    key_words = forms.CharField(max_length = 50, required = True)


class ProfileForm(forms.ModelForm):

	profile_img = cloudinary.forms.CloudinaryField()

	class Meta:
		model = ExtraProfile
		exclude = ('role', 'register_time','user','position')
		widget = {
			'profile_img':forms.FileInput,
		}

	def __init__(self,*args,**kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['profile_img'].required = False

