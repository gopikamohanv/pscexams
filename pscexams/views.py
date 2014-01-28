from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth
from pscexams.user_type import UserType
from pscexams.student.models import UserProfile
from pscexams.admin.models import State, Question
from pscexams.forms import FreeRegistration


# Index page for pscexams
def index(request):
	response = {}
	response.update({'states':State.objects.all()})
	return render_to_response('index.html', response)

#UserLogin
def login_view(request):
	response={}

	if request.method == 'GET':
		return HttpResponseRedirect('/')
	
	if 'username' in request.POST and request.POST['username']:
		username = request.POST['username']
	else:
		response.update({'no_username':True})

	if 'password' in request.POST and request.POST['password']:
		password = request.POST['password']
	else:
		response.update({'no_password':True})

	user = auth.authenticate(username=username,password=password)
	if user is not None and user.is_active:
		auth.login(request,user)
		return HttpResponseRedirect('/home/')
	elif user is None:
		no_user=True
		response.update({'no_user':no_user})
		return render_to_response('index.html',response)
	else:
		inactive_error=True
		response.update({'inactive':inactive_error})
		return render_to_response('index.html',response)

def logout_view(request):
		auth.logout(request)
		return HttpResponseRedirect('/')

# For redirecting according to usertype
def home(request):
	response={}
	response.update(csrf(request))
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		raise Http404()

	response.update({'user':user_profile})

	if user_profile.user_type == UserType.types['Tutor']:
		questions = Question.objects.filter(tutor=request.user)
		response.update({'questions':questions})
		return render_to_response('tutor_home.html',response)

	if user_profile.user_type == UserType.types['Student']:
		return HttpResponseRedirect('/student/dashboard/')

# Free Registration
def register(request):
	response = {}
	response.update({'states':State.objects.all()})

	if request.method == 'GET':
		return HttpResponseRedirect('/')

	form = FreeRegistration(request.POST)
	if form.is_valid():

		response.update({'form':form})
		try:
			state = State.objects.get(pk=form.cleaned_data['state'])
		except:
			response.update({'error':True})
			return render_to_response('index.html', response)

		try:
			user = User.objects.get(username=form.cleaned_data['username'])
			response.update({'user_error':True})
			return render_to_response('index.html', response)
		except:
			user = User.objects.create(username=form.cleaned_data['username'], first_name=form.cleaned_data['name'])
			user.set_password(form.cleaned_data['password'])
			user.save()

		userprofile = UserProfile.objects.create(user=user, mobile_no=form.cleaned_data['mobile'], state=state, user_type=UserType.types['Student'])
		try:
			userprofile.save()
		except:
			user.delete()
			response.update({'error':True})
			return render_to_response('index.html', response)

		userlogin = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
		auth.login(request,userlogin)
		return HttpResponseRedirect('/home/')

	response.update({'form':form})
	return render_to_response('index.html', response)