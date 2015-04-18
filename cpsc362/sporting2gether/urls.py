from django.conf.urls import patterns, url
from sporting2gether import views

urlpatterns = patterns('',
	#url(r'^your-name/?$', views.get_name, name='your-name'),
	url(r'^register/?$', views.user_register, name='register'),
	url(r'^login/?$', views.user_login, name='login'),
	url(r'^logout/?$', views.user_logout, name='logout'),
	url(r'^contact/?$', views.contact, name='contact'),
	url(r'^createevent/?$', views.create_event, name='create_event'),
	url(r'^event/?', views.view_events, name='view_event'),
	url(r'^', views.index, name='index'),
)
