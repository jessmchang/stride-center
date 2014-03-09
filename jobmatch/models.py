from django.contrib.auth.models import User
from django.db import models
from localflavor.us.models import USStateField
import requests

class Location(models.Model):
	address = models.CharField(blank=False, max_length=200)

	def get_lat_lng(self):
		if self.lat and self.lng:
			return (self.lat, self.lng)
		data = {'address' : self.address, 'sensor' : 'false'}
		resp = requests.get("http://maps.googleapis.com/maps/api/geocode/json", params=data).json()
		if (resp['status']!='OK'):
			raise Exception('Invalid address')
		self.lat = resp.geometry.lat
		self.lng = resp.geometry.lng
		return (self.lat, self.lng)

	def __str__(self):
		return self.address

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

	def __init__(self, *args, **kwargs):
		super(Job, self).__init__(*args, **kwargs)

	def __str__(self):
		return self.company.name + ': ' + self.title


# a job a student gained from a 3rd party
class StudentJob(Job):
	benefits = models.TextField()

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	# custom fields
	address = models.ForeignKey(Location)
	phone = models.IntegerField()

	# looking for part/full time jobs
	full_time = models.BooleanField()
	part_time = models.BooleanField()

	# entry-level or advanced?
	entry_level = models.BooleanField()

	# resume = models.FileField()

	# location student is interested in finding jobs in
	# location = 

	jobs = models.ManyToManyField(StudentJob)