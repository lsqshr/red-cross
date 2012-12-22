from django import forms
from django.forms.extras.widgets import SelectDateWidget

from red_cross_project.models import ExtraProfile

import account.forms


class SignupForm(account.forms.SignupForm):

    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))


class SearchForm(forms.Form):

    key_words = forms.CharField(max_length = 50, required = True)


class ProfileForm(forms.ModelForm):

	class Meta:
		model = ExtraProfile
		exclude = ('role', 'register_time','user')
