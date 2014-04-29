from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os.path
import datetime

from pscexams.user_type import UserType
from pscexams.admin.models import *
from pscexams.student.models import UserProfile
from pscexams.center.models import *


def center_check(user):
	try:
		user_profile = UserProfile.objects.get(user=user)
	except:
		return False
	if user_profile.user_type == UserType.types['Center']:
		return True
	else:
		return False

@login_required
@user_passes_test(center_check)
def center_dashboard(request):
	response = {}
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		raise Http500
	response.update({'user_profile':user_profile})
	return render_to_response('center_home.html', response)


@login_required
@user_passes_test(center_check)
def center_add_users(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})

	if request.method == 'GET':
		return render_to_response('add_users.html', response)

	if request.method == 'POST':
		form_error = False
		if 'name' in request.POST and request.POST['name']:
			name=request.POST['name']
		else:
			form_error = True
        
        if 'username' in request.POST and request.POST['username']:
            username=request.POST['username']
        else:
        	form_error = True   
            
        if 'password' in request.POST and request.POST['password']:
            password=request.POST['password']
        else:
        	form_error = True

        if 'email' in request.POST and request.POST['email']:
            email=request.POST['email']
        else:
        	form_error = True       

        if 'mobile' in request.POST and request.POST['mobile']:
            mobile_no=request.POST['mobile']
        else:
        	form_error = True

       	if 'state' in request.POST and request.POST['state']:
            state=request.POST['state']
        else:
        	form_error = True 


        if form_error:
			response.update({'form_error':True})
			return render_to_response('add_center.html', response)  
			 
        try:
            user_obj=User.objects.get(username=username)
            response.update({'reg_error':True})
            return render_to_response('add_users.html', response)
        except:
            user_obj=User(username=username, first_name=name, email=email, is_active=False)
            user_obj.set_password(password)
            user_obj.save();
            center_obj=Center(student=User.objects.get(id=user_obj.id), center=User.objects.get(id=request.user.id))
            center_obj.save();
            userprofiles_obj=UserProfile(user=User.objects.get(id=user_obj.id), user_type = 4, state=State.objects.get(id=state), mobile_no=mobile_no)      
            try:
            	userprofiles_obj.save();
            	response.update({'saved':True})
            except:
                raise Http404()

        return render_to_response('add_users.html', response)
	