from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required

def is_admin(request):
	return user.is_staff

def create_user(request):
	create_user(request.POST['username'], request.POST['email'], request.POST['password'])

def create_admin(request):
	create_superuser(request.POST['username'], request.POST['email'], request.POST['password'])

def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		#send them an error

def logout_user(request):
	# logout(request)

def email_user(request):
	request.POST['user'].email_user(request.POST['subject'], request.POST['message'])