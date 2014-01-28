from django import forms

class FreeRegistration(forms.Form):
	name = forms.CharField(max_length=255)
	username = forms.CharField(max_length=255)
	password = forms.CharField(max_length=255)
	mobile = forms.CharField(min_length=10, max_length=10)
	state = forms.CharField(max_length=10)