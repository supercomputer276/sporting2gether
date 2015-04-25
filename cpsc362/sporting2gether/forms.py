from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from sporting2gether.models import Users, Event
from django.db.models import Q

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=128)

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2',)

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

class PasswordResetForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='E-mail address', max_length=50, required=True)
	
	def is_valid(self):
		valid = super(PasswordResetForm,self).is_valid()
		if not valid:
			return valid
		#make sure username and e-mail correspond
		try:
			check = User.objects.get(Q(username=self.cleaned_data['username']))
		except User.DoesNotExist:
			self._errors['username'] = self.error_class(['User does not exist'])
			return False
		#check = User.objects.get(username=self.username)
		if check.email != self.cleaned_data['email']:
			self._errors['email'] = self.error_class(['User and Email do not match'])
			return False
		return True
	
class ProfileEditForm(forms.Form):
	newfirstname = forms.CharField(label="First name", max_length=30, required=False)
	newpassword = forms.CharField(label='New password', widget=forms.PasswordInput(), max_length=128, required=False, help_text="If you change your password, you will have to log back in after submitting your changes")
	newphone = forms.CharField(label="Phone # (digits)", max_length=10, required=False)
	confirmpassword = forms.CharField(label='Enter current password', widget=forms.PasswordInput(), max_length=128)

class EventEditForm(forms.ModelForm):
	start_datetime = forms.CharField(label='Date & Time', help_text='YYYY-MM-DD HH:MM (24-hour clock)')
	#kick = forms.MultipleChoiceField(choices=, label='', required=False)
	
	def __init__(self, thisevent, *args, **kwargs):
		super(EventEditForm, self).__init__(*args, **kwargs)
		self.fields['kick'] = forms.MultipleChoiceField(choices=[ (o.id, str(o)) for o in thisevent.participants.all()], required=False, widget=forms.CheckboxSelectMultiple())
	
	class Meta:
		model = Event
		fields = {'title', 'description', 'start_datetime', 'capacity', 'category', 'location_main', 'location_city', 'location_zip', 'is_cancelled'}