from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
	address = models.CharField(max_length=50)
	zipcode = models.IntegerField()
	city = models.CharField(max_length=25)
	state = models.CharField(max_length=25)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	# custom fields
	address = models.ForeignKey(Address)
	cellphone = models.IntegerField()

	# looking for part/full time jobs
	full_time = models.BooleanField()
	part_time = models.BooleanField()

	# entry-level or advanced?
	entry_level = models.BooleanField()

	# location
	# location = 

class Company(models.Model):
	name = models.CharField(max_length=50)

class Job(models.Model):
	company = models.ForeignKey(Company)
	full_time = models.BooleanField()
	title = models.CharField(max_length=50)
	salary = models.IntegerField()
	description = models.CharField(max_length=800)
