from django import forms
from django.forms.utils import flatatt
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from sporting2gether.models import Users, Event
from django.db.models import Q
from django.utils import timezone
from django.utils.html import format_html
from datetime import datetime#, timezone
#import pytz
#from django.contrib.admin.widgets import AdminSplitDateTime

class DateTimePickerWidget(forms.Widget):
	class Media:
		css = {
			'all': ('sporting2gether/bootstrap-datetimepicker.min.css',)
		}
		js = ('sporting2gether/jquery-2.1.3.min.js',
			'sporting2gether/moment.js',
			'sporting2gether/bootstrap.js',
			'sporting2gether/bootstrap-datetimepicker.js',)
	
	def render(self, name, value, attrs=None):
		if value is None:
			value = ''
		final_attrs = self.build_attrs(attrs, type='text', name=name)
		if value != '':
			final_attrs['value'] = value
		print final_attrs
		return format_html('<input{} /> <script type="text/javascript"> $(function () {' + '$(\'#{}\').datetimepicker({ format: \'YYYY-MM-DD HH:MM\', sideBySide: true }); }); </script>', flatatt(final_attrs), final_attrs['id'])

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
	start_datetime = forms.CharField(label='Start Date & Time',
		#widget=DateTimePickerWidget(),
		help_text='YYYY-MM-DD HH:MM (24-hour clock)')#widget=forms.SplitDateTimeWidget(),
	end_datetime = forms.CharField(label='End Date & Time',
		#widget=DateTimePickerWidget(),
		help_text='YYYY-MM-DD HH:MM (24-hour clock)', required=False)#widget=forms.SplitDateTimeWidget(),
	
	class Meta:
		model = Event
		fields = ('title', 'category', 'description', 'start_datetime', 'end_datetime', 'capacity', 'location_main', 'location_city', 'location_zip',)
	
	def is_valid(self):
		valid = super(CreateEventForm,self).is_valid()
		if not valid:
			return valid
		#events must start in the future (after / greater than now); as well, end time (if set) must be after start time
		starttime = datetime.strptime(self.cleaned_data['start_datetime'], "%Y-%m-%d %H:%M")
		if self.cleaned_data['end_datetime'] != '':
			endtime = datetime.strptime(self.cleaned_data['end_datetime'], "%Y-%m-%d %H:%M")
		else:
			endtime = starttime
		print starttime
		print endtime
		if starttime < datetime.now():
			self._errors['start_datetime'] = self.error_class(['You are not a time traveler. You cannot create events in the past.'])
			return False
		if endtime < starttime:
			self._errors['end_datetime'] = self.error_class(['An event\'s end time must be AFTER its start time.'])
			return False
		return True

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
	newshowemail = forms.BooleanField(label="Show e-mail to other users?", required=False)
	confirmpassword = forms.CharField(label='Enter current password', widget=forms.PasswordInput(), max_length=128)

class EventEditForm(forms.ModelForm):
	start_datetime = forms.CharField(label='Date & Time', help_text='YYYY-MM-DD HH:MM (24-hour clock)')
	end_datetime = forms.CharField(label='End Date & Time',
		#widget=DateTimePickerWidget(),
		help_text='YYYY-MM-DD HH:MM (24-hour clock)', required=False)#widget=forms.SplitDateTimeWidget(),
	#kick = forms.MultipleChoiceField(choices=, label='', required=False)
	
	def __init__(self, thisevent, *args, **kwargs):
		super(EventEditForm, self).__init__(*args, **kwargs)
		self.fields['kick'] = forms.MultipleChoiceField(choices=[ (o.id, str(o)) for o in thisevent.participants.all()], required=False, widget=forms.CheckboxSelectMultiple())
	
	def is_valid(self):
		valid = super(EventEditForm,self).is_valid()
		if not valid:
			return valid
		print '---FLAG 3---'
		#events must start in the future (after / greater than now); as well, end time (if set) must be after start time
		starttime = datetime.strptime(self.cleaned_data['start_datetime'], "%Y-%m-%d %H:%M")
		if self.cleaned_data['end_datetime'] == '':
			endtime = starttime
		elif self.cleaned_data['end_datetime'] is None:
			endtime = starttime
		else:
			try:
				endtime = datetime.strptime(self.cleaned_data['end_datetime'], "%Y-%m-%d %H:%M")
			except TypeError:
				endtime = self.cleaned_data['end_datetime']
		print starttime
		print endtime
		if timezone.is_naive(starttime):
			timezone.make_aware(starttime, timezone.get_current_timezone())
		if timezone.is_naive(endtime):
			timezone.make_aware(endtime, timezone.get_current_timezone())
		if starttime < datetime.now():
			self._errors['start_datetime'] = self.error_class(['You are not a time traveler. You cannot create events in the past.'])
			return False
		if endtime.isoformat() < starttime.isoformat():
			self._errors['end_datetime'] = self.error_class(['An event\'s end time must be AFTER its start time.'])
			return False
		return True
	
	class Meta:
		model = Event
		fields = {'title', 'description', 'start_datetime', 'end_datetime', 'capacity', 'category', 'location_main', 'location_city', 'location_zip', 'is_cancelled'}