from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth
from pscexams.user_type import UserType
from pscexams.student.models import *
from pscexams.admin.models import *

# Index page for pscexams
def index(request):
	return render_to_response('index.html')

#UserLogin
def login(request):
	response={}
	
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

	if user_profile.user_type == UserType.types['student']:
		response.update({'student_home.html', response})		    


