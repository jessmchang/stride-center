from django.contrib import admin
from jobmatch.models import Job, Company, Location

admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Location)