from django.contrib.auth.models import User
from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from localflavor.us.models import USStateField
from haversine import haversine
import requests

class Location(models.Model):
	address = models.CharField(blank=False, max_length=200)

	def get_lat_lng(self):
		if hasattr(self, 'lat') and hasattr(self, 'lng'):
			return (self.lat, self.lng)
		data = {'address' : self.address, 'sensor' : 'false'}
		resp = requests.get("http://maps.googleapis.com/maps/api/geocode/json", params=data).json()
		if (resp['status']!='OK'):
			raise Exception('Invalid address')
		self.lat = resp[u'results'][0][u'geometry'][u'location'][u'lat']
		self.lng = resp[u'results'][0][u'geometry'][u'location'][u'lng']
		return (self.lat, self.lng)

	def __str__(self):
		return self.address


class UserLocationRange(models.Model):
	zipcode = models.IntegerField(blank=True, null=True)
	# of miles from zipcode
	radius = models.IntegerField(blank=False, default=20)

	def get_lat_lng(self):
		if hasattr(self, 'lat') and hasattr(self, 'lng'):
			return (self.lat, self.lng)
		data = {'address' : self.zipcode, 'sensor' : 'false'}
		resp = requests.get("http://maps.googleapis.com/maps/api/geocode/json", params=data).json()
		if (resp['status']!='OK'):
			raise Exception('Invalid address')
		print(resp)
		self.lat = resp[u'results'][0][u'geometry'][u'location'][u'lat']
		self.lng = resp[u'results'][0][u'geometry'][u'location'][u'lng']
		return (self.lat, self.lng)

	def is_in_radius(self, job_location):
		return haversine(self.get_lat_lng(), job_location.get_lat_lng(), miles=True) < self.radius

	def __str__(self):
		return str(self.zipcode) + ', ' + str(self.radius) + ' mi'

class Company(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Job(models.Model):
	company = models.ForeignKey(Company)
	location = models.OneToOneField(Location)
	full_time = models.BooleanField()
	title = models.CharField(max_length=50)
	salary = models.IntegerField()
	description = models.TextField(max_length=800)

	def __str__(self):
		return self.company.name + ': ' + self.title

def send_match_emails(sender, instance, created, **kwargs):
	if created:
		profiles = UserProfile.objects.all()
		for profile in profiles:
			if profile.location_range.zipcode and profile.location_range.is_in_radius(instance.location):
				send_mail('New Job Opportunity!', 'Check out this cool new job.', 'stridecenter1@gmail.com',
				[profile.user.email], fail_silently=False)

post_save.connect(send_match_emails, sender=Job)

# a job a student gained from a 3rd party
class StudentJob(Job):
	benefits = models.TextField()

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	# contact info
	address = models.ForeignKey(Location, blank=True, null=True)
	phone = models.IntegerField(blank=True, null=True)

	# looking for part/full time jobs
	full_time = models.BooleanField(default=True)
	part_time = models.BooleanField(default=False)

	# experience level
	entry_level = models.BooleanField(default=True)
	advanced = models.BooleanField(default=False)

	resume = models.FileField(upload_to='resumes/%Y/%m/%d', blank=True, null=True)

	# notifications
	text_notifications = models.BooleanField(default=False)
	email_notifications = models.BooleanField(default=False)

	# currently searching for a job
	currently_searching = models.BooleanField(default=True)

	# location student is interested in finding jobs in
	location_range = models.OneToOneField(UserLocationRange)

	jobs = models.ManyToManyField(StudentJob, blank=True, null=True)

	def create_user_profile(sender, instance, created, **kwargs):
		# only create profile for non-admins
	    if created and not instance.is_staff:
	    	location_range = UserLocationRange()
	    	location_range.save()
	        UserProfile.objects.create(user=instance, location_range=location_range)

	post_save.connect(create_user_profile, sender=User)