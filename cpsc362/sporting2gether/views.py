from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	context_dict = {'page_title': 'Index'}
	return render(request, 'sporting2gether/index.html', context_dict)
