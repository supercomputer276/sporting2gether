from django.conf.urls import patterns, url
from sporting2gether import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)
