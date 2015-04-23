from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Users(models.Model):
	user = models.OneToOneField(User)
	phone_no = models.CharField(max_length=10,verbose_name="Phone # (digits)",blank=True)
	def __unicode__(self):
		return self.user.username

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
	creator = models.ForeignKey(User, related_name='event_creator')
	description = models.TextField()
	start_datetime = models.DateTimeField(verbose_name="Date & Time")
	capacity = models.PositiveIntegerField()
	category = models.CharField(max_length=4, choices=SPORT_CHOICES, verbose_name="Sport")
	location_main = models.CharField(max_length=50, verbose_name="Address")
	location_city = models.CharField(max_length=25, verbose_name="City")
	location_zip = models.CharField(max_length=5, verbose_name="ZIP Code")
	participants = models.ManyToManyField(User, related_name='event_players')
	is_cancelled = models.BooleanField(default=False)
	def __str__(self):
		return "Event: " + self.title
	
	def getDateTime(self):
		return datetime.combine(self.start_datetime.date(),self.start_datetime.time())
	
	def getTimeDifference(self):
		return datetime.today() - self.getDateTime()