from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sporting2gether import forms

#Holds context data for every page; update context_dict in each method with this
commonContext= {'login_form': forms.LoginForm()}

def index(request):
	context_dict = {'page_title': 'Index', 'page_template': 'sporting2gether/index.html'}
	context_dict.update(commonContext)
	return render_to_response('sporting2gether/page.html', context_dict, context_instance=RequestContext(request))

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.NameForm()

	context_dict = {'page_title': 'Name (Test)', 'page_template': 'sporting2gether/name.html', 'form': form}
	context_dict.update(commonContext)
    return render_to_response('sporting2gether/page.html', context_dict, context_instance=RequestContext(request))

def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = forms.UserForm(data=request.POST)
		profile_form = forms.UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
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
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.GET['next'] is not None:
					return HttpResponseRedirect(request.GET['next'])
				else:
					return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your Sporting 2gether account is disabled. Sorry.");
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResonse("Invalid login details supplied.")
	else:
		context_dict = {'page_title': 'Login', 'page_template': 'sporting2gether/login.html'}
		context_dict.update(commonContext)
		return render_to_response('sporting2gether/page.html', context_dict, context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')