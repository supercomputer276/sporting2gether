from django.conf.urls import patterns, url
from sporting2gether import views

urlpatterns = patterns('',
	url(r'^(?:index/?)?$', views.index, name='index'),
	url(r'^register/?$', views.user_register, name='register'),
	url(r'^login/?$', views.user_login, name='login'),
	url(r'^logout/?$', views.user_logout, name='logout'),
	url(r'^contact/?$', views.contact, name='contact'),
	url(r'^createevent/?$', views.create_event, name='create_event'),
	url(r'^event/view(/?(?P<eventid>\d+)/?)?$', views.event_detail, name='event_detail'),
	url(r'^event/edit/(?P<eventid>\d+)/?$', views.edit_event, name='edit_event'),
	url(r'^event/performsearch/?$', views.search_events, name='search_events'),
	url(r'^event/join/(?P<eventid>\d+)/?$', views.join_event, name='join_event'),
	url(r'^event(/?(?P<filter>\w+)(/?(?P<searchterm>\w+)/?)?)?', views.view_events, name='view_event'),
	url(r'^profile/edit/?$', views.edit_profile, name='edit_profile'),
	url(r'^profile(/?(?P<entry>\w+)/?)?$', views.show_profile, name='profile'),
	url(r'^resetpassword/?$', views.reset_password, name='reset_password'),
)
