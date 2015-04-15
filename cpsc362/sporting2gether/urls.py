from django.conf.urls import patterns, url
from sporting2gether import views

urlpatterns = patterns('',
	url(r'^your-name/?$', views.get_name, name='your-name'),
	url(r'^register/?$', views.register, name='register'),
	url(r'^login/?$', views.user_login, name='login'),
	url(r'^logout/?$', views.user_logout, name='logout'),
	url(r'^', views.index, name='index'),
)
