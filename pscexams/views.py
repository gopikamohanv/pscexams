from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import logout as auth_logout

from pscexams.user_type import UserType
from pscexams.student.models import *
from pscexams.admin.models import *

# Index page for pscexams
#/
def index(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})
	return render_to_response('index.html', response)

# For About Us page
#/about/ 
def about(request):
    response = {}
    return render_to_response('about.html')

# Description of smartindia
#/smartindia/
def smartindia(request):
    response = {}
    return render_to_response('smartindia.html')

# Description of kerala PSC exams
#/keralapsc/
def keralapsc(request):
    response = {}
    return render_to_response('keralapsc.html')

#UserLogin
#/login/
def user_login(request):
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
#/home/
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




#save new user details
#/registration/
def registration_add(request):
    response={}

    states = State.objects.all()
    response.update({'states':states})

    if request.method == 'GET':
        return render_to_response('registration.html', response)

    if request.method == 'POST':
    
        if 'name' in request.POST and request.POST['name']:
            name=request.POST['name']   
        
        if 'username' in request.POST and request.POST['username']:
            username=request.POST['username']   
            
        if 'password' in request.POST and request.POST['password']:
            password=request.POST['password']       
            
        if 'conassword' in request.POST and request.POST['conpassword']:
            con_password=request.POST['conpassword']        
        
        if 'email' in request.POST and request.POST['email']:
            email=request.POST['email']     

        if 'mobile' in request.POST and request.POST['mobile']:
            mobile_no=request.POST['mobile']

        if 'state' in request.POST and request.POST['state']:
            state=request.POST['state'] 
        
        
            
        user_obj=User() 
        user_obj.username=username
        user_obj.email=email
        user_obj.set_password(password)
        user_obj.is_active=True 
        user_obj.save();
        try:
            userprofiles_obj=UserProfile()      
        except:
            raise Http404("")
        
        userprofiles_obj.user=User.objects.get(id=user_obj.id)
        userprofiles_obj.name=name  
        userprofiles_obj.email=email
        userprofiles_obj.state=State.objects.get(id=state)    
        userprofiles_obj.mobile=mobile_no
        userprofiles_obj.user_type = 4
        try:
            userprofiles_obj.save();
            response.update({'success':True})
        except:
            raise Http404()
        
        return render_to_response('registration.html',response)


# Ajax for changing exam based on states
#/state/ajax/exam/
def state_ajax_exam(request):
	if 'state' in request.GET and request.GET['state']:
		state = request.GET['state']
		exams = Exam.objects.filter(state=state)
		response = '<option value=\"0\">Select Exams</option>'
		for exam in exams:
			response += '<option value=\"'
			response += str(exam.id)
			response += '\">'
			response += exam.exam
			response += '</option>'
		return HttpResponse(response)
	else:
		return HttpResponse('Error# No State Specified')


# Ajax for changing subject based on exam
#/exam/ajax/subject/
def exam_ajax_subject(request):
	if 'exam' in request.GET and request.GET['exam']:
		exam = request.GET['exam']
		subjects = Subject.objects.filter(exam=exam)
		response = '<option value=\"0\">Select Subject</option>'
		for subject in subjects:
			response += '<option value=\"'
			response += str(subject.id)
			response += '\">'
			response += subject.subject
			response += '</option>'
		return HttpResponse(response)
	else:
		return HttpResponse('Error# No State Specified')


# Ajax for changing topic based on subjects
#/subject/ajax/topic/
def subject_ajax_topic(request):
	if 'subject' in request.GET and request.GET['subject']:
		subject = request.GET['subject']
		topics = Topics.objects.filter(subject=subject)
		response = '<option value=\"0\">Select Topics</option>'
		for topic in topics:
			response += '<option value=\"'
			response += str(topic.id)
			response += '\">'
			response += topic.topic
			response += '</option>'
		return HttpResponse(response)
	else:
		return HttpResponse('Error# No State Specified')


# For logout
#/logout/
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')