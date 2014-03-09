from django import forms
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

class RegisterForm(forms.Form):
	email = forms.CharField(max_length=100)
	password = forms.CharField(max_length=16)
	conf_password = forms.CharField(max_length=16)

def index(request):
	if request.POST:
		pass
	else: 
		register_form = RegisterForm()

	return render_to_response('index.html', 
		{ 'register_form': register_form }, 
		context_instance=RequestContext(request))

def is_admin(request):
	return user.is_staff

def create_user(request):
	if request.POST:
		user = create_user(request.POST['email'], request.POST['email'], request.POST['password'])
		login(request, user)
		redirect('dashboard')

@login_required
def dashboard(request):
	return render_to_response('dashboard.html')

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
		pass

def logout_user(request):
	# logout(request)
	pass

def email_user(request):
	request.POST['user'].email_user(request.POST['subject'], request.POST['message'])