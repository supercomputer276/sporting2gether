from django import forms
from django.contrib.auth.models import User
from sporting2gether.models import Users, Event

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

class ContactForm(forms.Form):
	name = forms.CharField(label='Name',max_length=30, required=True)
	email = forms.EmailField(label='E-mail address', max_length=50, required=True)
	subject = forms.CharField(label='Subject',max_length=60, required=True)
	message = forms.CharField(label='Message',widget=forms.Textarea(), required=True)

class CreateEventForm(forms.ModelForm):
	start_datetime = forms.CharField(label='Date & Time', help_text='YYYY-MM-DD HH:MM (24-hour clock)')#widget=forms.SplitDateTimeWidget(),
	
	class Meta:
		model = Event
		fields = ('title', 'category', 'description', 'start_datetime', 'capacity', 'location_main', 'location_city', 'location_zip',)