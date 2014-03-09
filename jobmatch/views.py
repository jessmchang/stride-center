from django import forms
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from jobmatch.models import *
from jobmatch.decorators import *

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=16, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=100)
	password = forms.CharField(min_length=6, max_length=16, widget=forms.PasswordInput)
	confirm_password = forms.CharField(min_length=6, max_length=16, widget=forms.PasswordInput)

	def clean(self):
	    password = self.cleaned_data.get('password')
	    confirm_password = self.cleaned_data.get('confirm_password')

	    if password != confirm_password:
	        raise forms.ValidationError("Passwords don't match")

	    return self.cleaned_data

def login(request):
	if request.POST:
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = authenticate(username=request.POST['email'], 
				password=request.POST['password'])
			login(request, user)
			return render_to_response('dashboard.html', 
				context_instance=RequestContext(request))
	else: 
		login_form = LoginForm()

	return render_to_response('index.html', 
		{ 'login_form': login_form },
		context_instance=RequestContext(request))

def register(request):
	if request.POST:
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user = User.objects.create_user(
				request.POST['email'], 
				request.POST['email'], 
				request.POST['password'])
			user.first_name=request.POST['first_name']
			user.last_name=request.POST['last_name']
			user.save()
			user = authenticate(
				username=request.POST['email'],
				password=request.POST['password'])
			login(request, user)
			return render_to_response('dashboard.html', 
				context_instance=RequestContext(request))
	else: 
		register_form = RegisterForm()

	return render_to_response('register.html', 
		{ 'register_form': register_form }, 
		context_instance=RequestContext(request))

def is_admin(request):
	return user.is_staff

def create_user(request):
	if request.POST:
		user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
		login(request, user)
		redirect('dashboard')

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

def email_user(request):
	request.POST['user'].email_user(request.POST['subject'], request.POST['message'])

def logout_user(request):
	logout(request)
	return render_to_response('index.html', context_instance=RequestContext(request))

@login_required
def dashboard(request):
	jobs = Job.objects.all()
	return render_to_response('dashboard.html', {'jobs': jobs}, 
		context_instance=RequestContext(request))

@login_required
def profile(request):
	return render_to_response('profile.html', {'user': request.user}, 
		context_instance=RequestContext(request))