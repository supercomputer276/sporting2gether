from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, timedelta
from sporting2gether import forms, models
from cpsc362 import settings
import string
import random
import re

#Holds context data for every page; update context_dict in each method with this
commonContext= {'login_form': forms.LoginForm(), 'DEBUG': settings.DEBUG,}

def index(request):
	context_dict = {'page_title': 'Index', 'page_template': 'sporting2gether/index.html'}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=RequestContext(request))

def user_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = forms.UserForm(data=request.POST)
		profile_form = forms.UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = forms.UserForm()
        profile_form = forms.UserProfileForm()
	context_dict = {'page_title': 'Register', 'page_template': 'sporting2gether/register.html',
	'user_form': user_form, 'profile_form': profile_form, 'registered': registered
	}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context)

def user_login(request):
	#ideally, this would be a passover from logging into the header, but just in case, it may also serve as an individual page
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context = RequestContext(request)
	check = request.GET is not None
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if check:
					return HttpResponseRedirect(request.GET.get('next','/'))
				else:
					return HttpResponseRedirect('/')
			else:
				context_dict = {'page_title': 'Disabled Account', 'page_template': 'sporting2gether/disabled.html'}
				context_dict.update(commonContext)
				return render_to_response('sporting2gether/page.html', context_dict, context)
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			context_dict = {'page_title': 'Login Failed', 'page_template': 'sporting2gether/loginfail.html'}
			context_dict.update(commonContext)
			return render_to_response('sporting2gether/page.html', context_dict, context)
	else:
		context_dict = {'page_title': 'Login', 'page_template': 'sporting2gether/login.html'}
		context_dict.update(commonContext)
		if check:
			context_dict.update({'nexttext': '?next=' + request.GET.get('next','/')})
		else:
			context_dict.update({'nexttext': '?next=/'})
		return render_to_response('sporting2gether/page.html', context_dict, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def contact(request):
	context = RequestContext(request)
	sentForm = False
	if request.method == 'POST':
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			name = request.POST.get('name','anonymous customer')
			email = request.POST.get('email','no@email.provided')
			subject = "Sporting2gether contact: " + request.POST['subject']
			message = "From " + name + " at " + email + ":\n\n" + request.POST['message']
			send_mail(subject, message, from_email=email, recipient_list=['sporting2gether@gmail.com'], fail_silently=False)
			sentForm = True
		else:
			print form.errors
	else:
		form = forms.ContactForm()
	context_dict = {'page_title': 'Contact Us', 'page_template': 'sporting2gether/contact.html', 'form': form, 'sentForm': sentForm}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

@login_required
def create_event(request):
	context = RequestContext(request)
	sentForm = False
	if request.method == 'POST':
		form = forms.CreateEventForm(request.POST)
		if form.is_valid():
			#process form
			e = models.Event()
			e.title = request.POST['title']
			e.description = request.POST['description']
			e.creator = request.user
			e.start_datetime = request.POST['start_datetime']
			e.capacity = request.POST['capacity']
			e.category = request.POST['category']
			e.location_main = request.POST['location_main']
			e.location_city = request.POST['location_city']
			e.location_zip = request.POST['location_zip']
			e.save()
			#END process form
			sentForm = True
		else:
			print form.errors
	else:
		form = forms.CreateEventForm()
	context_dict = {'page_title': 'Create New Event', 'page_template': 'sporting2gether/createevent.html', 'form': form, 'sentForm': sentForm}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

def view_events(request,filter,searchterm):
	context = RequestContext(request)
	#build queryset
	target = ''
	sportchoices = models.Event.SPORT_CHOICES
	if filter is not None:
		if filter.lower() == "all":
			data = models.Event.objects.all()
		elif filter.lower() == "my":
			#events the user has hosted
			if request.user.is_authenticated():
				data = models.Event.objects.filter(creator=request.user)
			else:
				return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + request.path)
		elif filter.lower() == "schedule":
			#events the user has joined
			if request.user.is_authenticated():
				data = models.Event.objects.filter(participants=request.user.id)
			else:
				return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + request.path)
		elif filter.lower() == "today":
			#events today or later
			data = models.Event.objects.filter(start_datetime__gt=datetime.now())
		elif filter.lower() == "search":
			#event search
			if searchterm is not None:
				#searchterm verified
				#filter by sport if searchterm is "sport__" + one of the four-letter abbreviations
				#filter by ZIP code if searchterm is "zip__" + a five-digit number
				#otherwise filter by name and/or location (force this search if it starts with "name__")
				if re.match(r'name__\w*',searchterm):
					target = searchterm.replace('name__','')
					data = models.Event.objects.filter(title__contains=target)
				elif re.match(r'user__\w*',searchterm):
					target = searchterm.replace('user__','')
					innerquery = User.objects.filter(username__contains=target)
					data = models.Event.objects.filter(creator__in=innerquery)
				elif re.match(r'sport__\w\w\w\w$',searchterm):
					target = searchterm.replace('sport__','')
					data = models.Event.objects.filter(category=target)
					for c in sportchoices:
						if c[0] == target:
							target = c[1]
				elif re.match(r'zip__\d\d\d\d\d$',searchterm):
					target = searchterm.replace('zip__','')
					data = models.Event.objects.filter(location_zip=target)
				else:
					#search event title if nothing else matches
					data = models.Event.objects.filter(title__contains=target)
			else:
				#show all data
				data = models.Event.objects.all()
		else:
			data = models.Event.objects.all()
	else:
		data = models.Event.objects.all()
	#END built queryset
	#number of entries
	data_number = data.count()
	#time until
	timeleft = []
	for e in data:
		e.start = e.getDateTime()
		temp = e.getTimeDifference()
		temp2 = abs(temp)
		text = "";
		#text += str(temp.days) + " days, " + str(temp.seconds/60/60) + " minutes, " + str(temp.seconds) + " seconds"
		#text += str(temp2)
		#temp.seconds delivers the number of seconds in the day
		#text += " | "
		if temp2 > timedelta(days=1):
			text += str(temp2.days) + " days"
		elif temp2 > timedelta(hours=1):
			text += str(temp2.seconds/3600) + " hours and " + str(temp2.seconds/60) + " minutes"
		elif temp2 > timedelta(minutes=1):
			text += str(temp2.seconds/60) + " minutes and " + str(temp2.seconds) + " seconds"
		else:
			text += str(temp2)
		
		if temp >= timedelta(0):
			#time ago
			text += " ago"
		else:
			#time until
			text += " until event"
		timeleft += [text]
	#END time until
	context_dict = {'page_title': 'Events', 'page_template': 'sporting2gether/eventlist.html',
		'data': data, 'data_number': data_number, 'CHOICES': sportchoices, 'timeleft': timeleft, 'filter': filter, 'searchtarget': target}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

def search_events(request):
	#store next page from GET
	nextpage = request.GET.get('next','/event/all')
	#search via POST
	if request.method == "POST":
		#determine which search was used
		nextpage = '/event/search/'
		if request.POST.get('submit_name',None) == "Search Event Name":
			nextpage += 'name__' + request.POST.get('search_name','') + '/'
		if request.POST.get('submit_user',None) == "Search User":
			nextpage += 'user__' + request.POST.get('search_user','') + '/'
		elif request.POST.get('submit_sport',None) == "Filter Sport":
			nextpage += 'sport__' + request.POST.get('search_sport','') + '/'
		elif request.POST.get('submit_zip',None) == "Search ZIP":
			nextpage += 'zip__' + request.POST.get('search_zip','') + '/'
		return HttpResponseRedirect(nextpage)
	else:
		return HttpResponseRedirect(nextpage)

def event_detail(request, eventid):
	context = RequestContext(request)
	#get relevant event
	thisevent = models.Event.objects.get(id=eventid)
	sportchoices = models.Event.SPORT_CHOICES
	#get join errors
	errormsg = ""
	if request.GET.get('error',None) is not None:
		errormsg += "<ul><li>"
		if request.GET.get('error',None) == '1':
			errormsg += "Sorry, the event filled up while you weren't looking."
		if request.GET.get('error',None) == '2':
			errormsg += "Sorry, the event was cancelled while you weren't looking."
		if request.GET.get('error',None) == '3':
			errormsg += "You're the host! You can't join your own event."
		errormsg += "</li></ul>"
	#is the user in this event
	joined = False
	if request.user.is_authenticated():
		joined = request.user in thisevent.participants.all()
	context_dict = {'page_title': 'Event Detail - ' + thisevent.title, 'page_template': 'sporting2gether/eventdetail.html',
		'thisevent': thisevent, 'CHOICES': sportchoices, 'errormsg': errormsg, 'joined': joined,}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

@login_required
def edit_event(request, eventid):
	context = RequestContext(request)
	#get relevant event
	thisevent = models.Event.objects.get(id=eventid)
	sportchoices = models.Event.SPORT_CHOICES
	#translate start_datetime
	timevalue =  thisevent.start_datetime.strftime("%Y-%m-%d %H:%M")
	#process form
	errormsg = ''
	sentForm = False
	if request.method == "POST":
		form = forms.EventEditForm(thisevent,request.POST)
		if form.is_valid():
			#save changes (except capacity)
			thisevent.title = request.POST.get('title',thisevent.title)
			thisevent.description = request.POST.get('description',thisevent.description)
			thisevent.start_datetime = request.POST.get('start_datetime',thisevent.start_datetime)
			thisevent.category = request.POST.get('category',thisevent.category)
			thisevent.location_main = request.POST.get('location_main',thisevent.location_main)
			thisevent.location_city = request.POST.get('location_city',thisevent.location_city)
			thisevent.location_zip = request.POST.get('location_zip',thisevent.location_zip)
			#cancelled flag
			thisevent.is_cancelled = request.POST.get('is_cancelled',False) #is not None
			#remove marked players from participation
			for target in request.POST.get('kick',[]):
				thisevent.participants.remove(target)
			#set capacity to higher of either POST number or participant number
			thisevent.capacity = request.POST.get('capacity',thisevent.capacity)
			if thisevent.participants.count() > thisevent.capacity:
				thisevent.capacity = thisevent.participants.count()
			thisevent.save()
			errormsg = '<p style="color:#008800;">Changes saved!</p>'
		else:
			errormsg = form.errors
	else:
		form = forms.EventEditForm(thisevent)
	context_dict = {'page_title': 'Event Edit - ' + thisevent.title, 'page_template': 'sporting2gether/eventedit.html',
		'thisevent': thisevent, 'CHOICES': sportchoices, 'timevalue': timevalue, 'form': form, 'errormsg': errormsg}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

@login_required
def join_event(request, eventid):
	#get relevant event
	thisevent = models.Event.objects.get(id=eventid)
	#check whether or not the user's ID is already in this page; add or remove as necessary
	if thisevent.creator != request.user:
		if not thisevent.is_cancelled:
			if request.user in thisevent.participants.all():
				#remove
				thisevent.participants.remove(request.user)
			elif thisevent.participants.count() < thisevent.capacity:
				thisevent.participants.add(request.user)
			else:
				#hit capacity!
				return HttpResponseRedirect('/event/view/' + str(thisevent.id) + '/?error=1') #1
			return HttpResponseRedirect('/event/view/' + str(thisevent.id) + '/')
		else:
			#cancelled!
			return HttpResponseRedirect('/event/view/' + str(thisevent.id) + '/?error=2') #2
	else:
		#host!
		return HttpResponseRedirect('/event/view/' + str(thisevent.id) + '/?error=3') #3

def show_profile(request,entry):
	context = RequestContext(request)
	data = models.Users.objects.all()
	#get one user profile based on the entry value
	if entry is not None:
		if entry.lower() == 'my':
			if request.user.is_authenticated():
				return HttpResponseRedirect('/profile/' + request.user.username + '/')
			else:
				return HttpResponseRedirect(settings.LOGIN_URL + '?next=' + request.path)
		else:
			#profile username
			check = User.objects.get(username=entry).id
			data = get_object_or_404(models.Users, user=check)
			#data = models.Users.objects.get(user=check)
	else:
		return HttpResponseRedirect('/profile/my/')
	context_dict = {'page_title': 'Profile', 'page_template': 'sporting2gether/profile.html',
		'data': data, 'entry': entry}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

@login_required
def edit_profile(request):
	context = RequestContext(request)
	wrongpasswordflag = False
	data = models.Users.objects.get(user=request.user)
	#get Users for this user
	if request.method == "POST":
		form = forms.ProfileEditForm(request.POST)
		if form.is_valid():
			check = request.POST['confirmpassword']
			if request.user.check_password(check):
				#save changes
				thing = data.user
				if form.cleaned_data['newphone'] != '':
					data.phone_no = request.POST.get('newphone',data.phone_no)
					data.save()
				if form.cleaned_data['newfirstname'] != '':
					thing.first_name = request.POST.get('newfirstname',thing.first_name)
					thing.save()
				if form.cleaned_data['newpassword'] != '':
					thing.set_password(request.POST['newpassword'])
					thing.save()
				return HttpResponseRedirect('/profile/my/')
			else:
				wrongpasswordflag = True
		else:
			print form.errors
	else:
		form = forms.ProfileEditForm()
	context_dict = {'page_title': 'Edit Profile', 'page_template': 'sporting2gether/editprofile.html',
		'form': form, 'data': data, 'wrongpasswordflag': wrongpasswordflag}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)

def reset_password(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	context = RequestContext(request)
	sentForm = False;
	if request.method == "POST":
		form = forms.PasswordResetForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			email_to = request.POST['email']
			#check that email belongs to that user
			check = User.objects.get(username=username)
			if check.email == email_to:
				#create new password
				newpassword = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(9))
				#set new password
				check.set_password(newpassword)
				check.save()
				#send new password
				subject = "Sporting2gether: password reset"
				message = "Hello! You're receiving this email because your password at Sporting 2gether has been reset.\n\n" + "Your new password is \"" + newpassword + "\" (without the quotes, of course). Once you have logged in, we recommend changing your password to something more memorable from your Profile page.\n\n" + "Sincerely,\n" + "the Sporting2gether team"
				send_mail(subject, message, from_email='sporting2gether@google.com', recipient_list=[email_to], fail_silently=False)
				sentForm = True
				
			else:
				return HttpResponse("Username and email do not match.")
		else:
			print form.errors
	else:
		form = forms.PasswordResetForm()
	context_dict = {'page_title': 'Password Reset', 'page_template': 'sporting2gether/resetpassword.html', 'form': form, 'sentForm': sentForm}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=context)