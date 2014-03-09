from django.contrib import admin
from jobmatch.models import Job, Company

admin.site.register(Company)
admin.site.register(Job)