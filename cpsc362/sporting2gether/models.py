from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
	user = models.OneToOneField(User)
	phone_no = models.CharField(max_length=10,verbose_name="Phone # (digits)")

class Event(models.Model):
	BASEBALL = 'BASE'
	BASKETBALL = 'BASK'
	VOLLEYBALL = 'VOLL'
	SOCCER = 'SOCC'
	FOOTBALL = 'FOOT'
	GOLF = 'GOLF'
	TENNIS = 'TENN'
	SWIMMING = 'SWIM'
	SKIING = 'SKII'
	SNOWBOARDING = 'SNOW'
	OTHER = 'OTHR'
	SPORT_CHOICES = (
		(BASEBALL, 'Baseball'),
		(BASKETBALL, 'Basketball'),
		(VOLLEYBALL,'Volleyball'),
		(SOCCER,'Soccer / Football'),
		(FOOTBALL,'American Football'),
		(GOLF,'Golf'),
		(TENNIS,'Tennis'),
		(SWIMMING,'Swimming'),
		(SKIING,'Skiing'),
		(SNOWBOARDING,'Snowboarding'),
		(OTHER,'Other'),
	)
	#Automatic primary key
	title = models.CharField(max_length=50)
	creator = models.ForeignKey(Users)
	description = models.TextField()
	start_datetime = models.DateTimeField(verbose_name="Date & Time")
	capacity = models.PositiveIntegerField()
	category = models.CharField(max_length=4, choices=SPORT_CHOICES, verbose_name="Sport")
	location_main = models.CharField(max_length=50)
	location_city = models.CharField(max_length=25)
	location_zip = models.CharField(max_length=5)


class Participation(models.Model):
	event = models.ForeignKey(Event)
	user = models.ForeignKey(Users)