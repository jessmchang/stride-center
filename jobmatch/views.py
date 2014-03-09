from django import forms
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from jobmatch.models import *
from jobmatch.decorators import *

class LoginForm(forms.Form):
	email = forms.EmailField(max_length=100)
	password = forms.CharField(max_length=16, widget=forms.PasswordInput)

	def clean(self):
		user = authenticate(username=self.cleaned_data.get('email'), 
				password=self.cleaned_data.get('password'))
		if (user is None):
			raise forms.ValidationError("Incorrect email/password combination")

		return self.cleaned_data

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


@public_only
def user_login(request):
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


def user_logout(request):
	logout(request)
	return render_to_response('index.html', context_instance=RequestContext(request))

@public_only
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

@login_required
def dashboard(request):
	jobs = Job.objects.all()
	return render_to_response('dashboard.html', {'jobs': jobs}, 
		context_instance=RequestContext(request))

@login_required
def profile(request):
	profile = request.user.get_profile()
	location_range = profile.location_range
	return render_to_response('profile.html', 
		{'user': request.user, 
		'profile': profile,
		'location_range': location_range}, 
		context_instance=RequestContext(request))

@login_required
def edit_prefs(request):
	if request.POST:
		profile = request.user.get_profile()
		profile.location_range.zipcode = int(request.POST['zipcode']) if request.POST['zipcode'] else profile.location_range.zipcode
		profile.location_range.radius = int(request.POST['range']) if request.POST['range'] else profile.location_range.radius
		profile.location_range.save()
		profile.save()
	return redirect('/profile/', {'user': request.user, 
		'profile': request.user.get_profile(),
		'location_range': request.user.get_profile().location_range})

@login_required
def update_contact(request):
	if request.POST:
		profile = request.user.get_profile()
		if request.POST.get('email', False): 
			user.email = request.POST['email']
		if request.POST.get('phone', False): 
			profile.phone = int(request.POST['phone'])
		if request.POST.get('address', False): 
			profile.address = request.POST['address']
		if request.FILES.get('resume', False): 
			profile.resume = request.FILES['resume']
		request.user.save()
		profile.save()
	return redirect('/profile/')