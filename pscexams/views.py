from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import logout as auth_logout

from pscexams.user_type import UserType
from pscexams.student.models import UserProfile
from pscexams.admin.models import State, Question, Exam, Subject, Topic, SubTopic, OnewordQuestion
from pscexams.forms import FreeRegistration


# Index page for pscexams
#/
def index(request):
	response = {}
	states = State.objects.all()
	exams = Exam.objects.all()
	response.update({'exams':exams})
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

	response.update({'user':request.user})

	if user_profile.user_type == UserType.types['Tutor']:
		return render_to_response('tutor_home.html',response)

	if user_profile.user_type == UserType.types['Student']:
		return HttpResponseRedirect('/student/dashboard/')

	if user_profile.user_type == UserType.types['Publisher']:
		return HttpResponseRedirect('/publisher/dashboard/')

	if user_profile.user_type == UserType.types['Admin']:
		return HttpResponseRedirect('/siteadmin/dashboard/')   


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
        
        
            
        user_obj=User(username=username, first_name=name, email=email, is_active=False)
        user_obj.set_password(password)
        user_obj.save();
        userprofiles_obj=UserProfile(user=User.objects.get(id=user_obj.id), user_type = 4, state=State.objects.get(id=state), mobile_no=mobile_no)      
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
		response = '<option value=\"0\">Select Exam</option>'
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
		topics = Topic.objects.filter(subject=subject)
		response = '<option value=\"0\">Select Topic</option>'
		for topic in topics:
			response += '<option value=\"'
			response += str(topic.id)
			response += '\">'
			response += topic.topic
			response += '</option>'
		return HttpResponse(response)
	else:
		return HttpResponse('Error# No State Specified')

# Ajax for changing topic based on subjects
#/subject/ajax/topic/
def topic_ajax_subtopic(request):
	if 'topic' in request.GET and request.GET['topic']:
		topic = request.GET['topic']
		sub_topics = SubTopic.objects.filter(topic=topic)
		response = '<option value=\"0\">Select Sub Topic</option>'
		for sub_topic in sub_topics:
			response += '<option value=\"'
			response += str(sub_topic.id)
			response += '\">'
			response += sub_topic.sub_topic
			response += '</option>'
		return HttpResponse(response)
	else:
		return HttpResponse('Error# No State Specified')


# Ajax for tutor question search
# /subtopic/ajax/add/question/
def subtopic_ajax_question(request):
	response = {}
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	try:
		questions = Question.objects.filter(tutor=request.user, sub_topic=sub_topic)
		response.update({'questions':questions})
	except:
		response.update({'no_questions':True})
	return render_to_response('ajax_questions.html', response)

# Ajax for tutor subtopic search
# /subtopic/ajax/oneword/	
def subtopic_ajax_oneword(request):
	response = {}
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	try:
		onewords = OnewordQuestion.objects.filter(tutor=request.user, sub_topic=sub_topic)
		response.update({'onewords':onewords})
	except:
		response.update({'no_questions':True})		
	return render_to_response('ajax_onewords.html', response)


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

# For About Previous year Questions
#/about/previous/year/question/ 
def about_previous_year_question(request):
    response = {}
    return render_to_response('about_previous_year_question.html')

# For About Model exams
#/about/modelexams/ 
def about_model_exams(request):
    response = {}
    return render_to_response('about_modelexams.html')

# For About Tips and Tricks
#/about/tipsandtricks/ 
def about_tipsandtricks(request):
    response = {}
    return render_to_response('about_tipsandtricks.html')

# For About Read and Learn
#/about/readandlearn/ 
def about_readandlearn(request):
    response = {}
    return render_to_response('about_readandlearn.html')

# For About New Exams
#/about/readandlearn/ 
def about_new(request):
    response = {}
    return render_to_response('about_new.html')

# For About Exam Categories
def about_examcategory(request):
	response = {}

	if 'id' in request.GET and request.GET['id']:
		exam_id = request.GET['id']

	try:
		exam = Exam.objects.get(id=exam_id)
	except:
		raise Http404()
	subjects = Subject.objects.filter(exam=exam_id)
	response.update({'subjects':subjects})
	response.update({'exam':exam})
	return render_to_response('about_examcategory.html',response)

# For Topics in Subjects
def about_subject_topics(request):
	response = {}

	if 'id' in request.GET and request.GET['id']:
		subject_id = request.GET['id']

	try:
		subject = Subject.objects.get(id=subject_id)
	except:
		raise Http404()
	topics = Topic.objects.filter(subject=subject)
	response.update({'topics':topics})
	response.update({'subject':subject})
	return render_to_response('about_topic_in_subject.html',response)

# For Sub-topics in topic
def about_topic_subtopic(request):
	response = {}

	if 'id' in request.GET and request.GET['id']:
		topic_id = request.GET['id']

	try:
		topic = Topic.objects.get(id=topic_id)
	except:
		raise Http404()
	sub_topics = SubTopic.objects.filter(topic=topic)
	response.update({'sub_topics':sub_topics})
	response.update({'topic':topic})
	return render_to_response('about_subtopic_in_topic.html',response)

	

