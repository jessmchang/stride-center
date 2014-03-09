from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.us.models import USStateField

class Location(models.Model):
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=25)
	state = USStateField()
	zipcode = models.IntegerField()

	def __str__(self):
		return self.address + ', ' + self.city + ', ' + self.state + ' ' + str(self.zipcode)

class Company(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Job(models.Model):
	company = models.ForeignKey(Company)
	location = models.ForeignKey(Location)
	full_time = models.BooleanField()
	title = models.CharField(max_length=50)
	salary = models.IntegerField()
	description = models.TextField(max_length=800)

	def __str__(self):
		return self.company.name + ': ' + self.title


# a job a student gained from a 3rd party
class StudentJob(Job):
	benefits = models.TextField()

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	# custom fields
	address = models.ForeignKey(Location)
	cellphone = models.IntegerField()

	# looking for part/full time jobs
	full_time = models.BooleanField()
	part_time = models.BooleanField()

	# entry-level or advanced?
	entry_level = models.BooleanField()

	# resume = models.FileField()

	# location
	# location = 

	jobs = models.ManyToManyField(StudentJob)