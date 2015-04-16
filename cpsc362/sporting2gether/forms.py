from django import forms
from django.contrib.auth.models import User
from sporting2gether.models import Users

#FORMS the application uses
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
	
class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=128)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ('phone_no',)