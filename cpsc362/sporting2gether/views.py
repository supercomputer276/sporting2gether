from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	context_dict = {'page_title': 'Index', 'page_template': 'sporting2gether/index.html'}
	return render(request, 'sporting2gether/page.html', context_dict)
