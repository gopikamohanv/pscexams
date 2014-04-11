from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth import logout as auth_logout
from django.core.mail import mail_admins
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import mail_admins
from django.core.mail import EmailMultiAlternatives

from pscexams.user_type import UserType
from pscexams.student.models import UserProfile
from pscexams.admin.models import State, Question, Exam, Subject, Topic, SubTopic, OnewordQuestion, ModelExam, ModelExamQuestionPaper, PreviousYearQuestionPaper, TipsandTricks
from pscexams.forms import FreeRegistration
from pscexams.sms import *

import random
import string
import json

# Index page for pscexams
#/
def index(request):
	response = {}
	states = State.objects.all()
	exams = Exam.objects.all()
	response.update({'exams':exams})
	response.update({'states':states})
	response.update({'index_page': True})
	return render_to_response('index.html', response)

# For About Us page
#/about/ 
def about(request):
    response = {}
    response.update({'sub_title': 'psc exams'})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about.html', response)

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
    exams = Exam.objects.all()
    response.update({'exams':exams})

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
			user = User.objects.create(username=form.cleaned_data['username'], first_name=form.cleaned_data['name'], email=form.cleaned_data['email'])
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
		
		subject = "PSC Exams"
		template_html = 'Dear ' + form.cleaned_data['name'] + ',  Thank you for registering in pscexams.com.<br><br>If you have any queries, mail us to info@pscexams.com.'
		msg = EmailMultiAlternatives(subject, template_html,'', [form.cleaned_data['email']])
		msg.attach_alternative(template_html, "text/html")
		msg.content_subtype = "html"
		msg.send()

		message = 'Dear ' + form.cleaned_data['username'] + ', Your account has been activated and is ready to use. For more support call 1800-123-2003 or write to info@pscexams.com'
		send_sms(message, form.cleaned_data['mobile'])

		return HttpResponseRedirect('/home/')

	response.update({'form':form})
	return render_to_response('index.html', response)



# For About Previous year Questions
#/about/previous/year/question/ 
def about_previous_year_question(request):
    response = {}
    response.update({'sub_title': 'Previous year questions'})
    states = State.objects.all()
    response.update({'states':states})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about_previous_year_question.html', response)

# For About Model exams
#/about/modelexams/ 
def about_model_exams(request):
    response = {}
    response.update({'sub_title': 'Model Question Papers'})
    states = State.objects.all()
    response.update({'states':states})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about_modelexams.html', response)

# For About Tips and Tricks
#/about/tipsandtricks/ 
def about_tipsandtricks(request):
    response = {}
    response.update({'sub_title': 'Tips and tricks for pscexams'})
    states = State.objects.all()
    response.update({'states':states})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about_tipsandtricks.html', response)

# For About Read and Learn
#/about/readandlearn/ 
def about_readandlearn(request):
    response = {}
    response.update({'sub_title': 'psc materials'})
    states = State.objects.all()
    response.update({'states':states})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about_readandlearn.html', response)

# For About New Exams
#/about/readandlearn/ 
def about_new(request):
    response = {}
    response.update({'sub_title': 'Last Grade Servants Exam'})
    states = State.objects.all()
    response.update({'states':states})
    exams = Exam.objects.all()
    response.update({'exams':exams})
    return render_to_response('about_new.html', response)

# For About Exam Categories
def about_examcategory(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})
	exams = Exam.objects.all()
	response.update({'exams':exams})

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
	states = State.objects.all()
	response.update({'states':states})
	exams = Exam.objects.all()
	response.update({'exams':exams})

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
	states = State.objects.all()
	response.update({'states':states})
	exams = Exam.objects.all()
	response.update({'exams':exams})

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


def contact(request):
	response = {}
	response.update({'sub_title': 'Contact'})
	response.update(csrf(request))
	exams = Exam.objects.all()
	response.update({'exams':exams})

	if request.method == 'GET':
		return render_to_response('contact.html', response)

	if request.method == 'POST':

		form_error = False
		if 'name' in request.POST and request.POST['name']:
			name = request.POST['name']
		else:
			form_error = True

		if 'email' in request.POST and request.POST['email']:
			email = request.POST['email']
		else:
			form_error = True

		if 'message' in request.POST and request.POST['message']:
			contact_message = request.POST['message']
		else:
			form_error = True

		usersubject = ''
		if 'subject' in request.POST and request.POST['subject']:
			usersubject = request.POST['subject']

		if form_error:
			response.update({'form_error':True})
			return render_to_response('contact.html', response)

		subject = "Pscexams Contact us Message"
		template_html = 'contact_mail.html'
		html_content = render_to_string(template_html,{'Name':name, 'Email':email, 'Message':contact_message, 'Subject':usersubject})
		msg = EmailMultiAlternatives(subject, template_html,'', ['info@pscexams.com'])
		msg.attach_alternative(html_content, "text/html")
		msg.content_subtype = "html"
		msg.send()

		response.update({'message_sent':True})
		return render_to_response('contact.html', response)

	return render_to_response('contact.html', response)


def list_modelexams_free(request):
	response = {}

	if 'id' in request.GET and request.GET['id']:
		exam_id = request.GET['id']
	else:
		form_error = True

	modelexams = ModelExam.objects.get(exam=exam_id)
	response.update({'modelexams':modelexams})

	return render_to_response('free_modelexams.html', response)
	

def list_tipsandtricks(request, pk):
	response = {}
	return render_to_response('list_tipsandtricks.html', response)

def free_practice(request):
	response = {}
	response.update({'sub_title': 'psc questions and answers'})
	response.update({'states':State.objects.all()})
	return render_to_response('free_practice.html', response)

def free_practice_test(request):
	response = {}
	response.update({'states':State.objects.all()})
	if 'topic' in request.GET and request.GET['topic']:
		topic = request.GET['topic']
	else:
		response.update({'no_topic': True})
		return render_to_response('free_practice.html', response)

	subject = get_object_or_404(Subject, pk=topic)
	response.update({'subject':subject})
	tests = range(1,11)
	response.update({'tests': tests})
	return render_to_response('free_practice_tests.html', response)

def free_practice_start(request, pk):
	response = {}
	subject = get_object_or_404(Subject, pk=pk)
	response.update({'subject':subject})
	response.update({'states':State.objects.all()})

	if 'test' in request.GET and request.GET['test']:
		test = request.GET['test']
	else:
		response.update({'no_test':True})
		return render_to_response('free_practice_start.html', response)
	if int(test)>10:
		response.update({'not_allowed':True})
		return render_to_response('free_practice_start.html', response)
	else:			
		page = int(test) - 1
	questions = Question.objects.filter(sub_topic__topic__subject=subject).order_by('-pk')[(page*10):(page*10)+10]

	if questions.count() < 10:
		pass
	else:
		response.update({'questions':questions})
	response.update({'test':test})
	return render_to_response('free_practice_start.html', response)

def ajax_practice_free(request):
	response = {}

	# Get POST values send from test 
	question_pk = request.POST.get('question', '-1')
	question = get_object_or_404(Question, pk=question_pk)
	option = request.POST.get('option', '-1')
	
	json_response = {}
	# Check the answer and give marks to the student
	score = 0
	if option == question.answer:
		score += 1
		img_url = "https://s3.amazonaws.com/uploads.smartindia/success-icon.png"
	else:
		img_url = "https://s3.amazonaws.com/uploads.smartindia/Cross-icon.png"	
	json_response['answer'] = question.answer 	
	json_response['score'] = score
	json_response['img_url'] = img_url
	json_response = json.dumps(json_response)
	return HttpResponse(json_response, 'application/json')	

def free_modelexam(request, pk):
	response = {}
	response.update({'states': State.objects.all()})	
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam': exam})
	response.update({'modelexams': ModelExam.objects.filter(exam=exam)})
	return render_to_response('free_modelexam_list.html', response)

def free_modelexam_download(request, pk):
	response = {}
	response.update({'states': State.objects.all()})
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	if 'id' in request.GET and request.GET['id']:
		modelexam_id = request.GET['id']
	else:
		response.update({'no_exam':True})
		return render_to_response('free_modelexam_download.html', response)
	modelexam = get_object_or_404(ModelExam, pk=modelexam_id)
	try:
		modelquestion = ModelExamQuestionPaper.objects.get(modelexam=modelexam)
		response.update({'modelquestion':modelquestion})
	except:
		response.update({'form_error': True})
	return render_to_response('free_modelexam_download.html', response)	

def free_previous_exam(request, pk):
	response = {}
	response.update({'states':State.objects.all()})
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	previous_exams = PreviousYearQuestionPaper.objects.filter(exam=exam)
	response.update({'previous_exams':previous_exams})
	return render_to_response('free_previous_exam_download.html', response)

def free_tricks(request, pk):
	response = {}
	response.update({'states':State.objects.all()})
	subject = get_object_or_404(Subject, pk=pk)
	response.update({'subject':subject})
	response.update({'tricks': TipsandTricks.objects.filter(sub_topic__topic__subject=subject).order_by('-pk')[:20]})
	return render_to_response('free_tricks.html', response)

def free_tricks_detail(request, pk):
	response = {}
	response.update({'states':State.objects.all()})
	subject = get_object_or_404(Subject, pk=pk)
	response.update({'subject':subject})
	response.update({'tricks': TipsandTricks.objects.filter(sub_topic__topic__subject=subject).order_by('?')[:10]})
	if 'id' in request.GET and request.GET['id']:
		trick_id = request.GET['id']
	else:
		response.update({'no_tricks': True})
		return render_to_response('free_tricks_detail.html', response)
	trick = get_object_or_404(TipsandTricks, pk=trick_id)
	response.update({'trick':trick})
	return render_to_response('free_tricks_detail.html', response)

def free_learn(request, pk):
	response = {}
	response.update({'states':State.objects.all()})
	subject = get_object_or_404(Subject, pk=pk)
	response.update({'subject': subject})
	response.update({'materials': OnewordQuestion.objects.filter(sub_topic__topic__subject=subject).order_by('-pk')[:100]})
	return render_to_response('free_materials.html', response)


def sub_topic_content(request):
	response = {}
	response.update({'states':State.objects.all()})
	if 'id' in request.GET and request.GET['id']:
		sub_topic_id = request.GET['id']

	if 'topic' in request.GET and request.GET['topic']:
		topic_id = request.GET['topic']

	sub_topic = SubTopic.objects.get(pk=sub_topic_id)
	sub_topics_in_topic = SubTopic.objects.filter(topic=topic_id).order_by('?')[:10]
	response.update({'sub_topics_in_topic':sub_topics_in_topic})
	response.update({'sub_topic':sub_topic})
	tipsandtricks = TipsandTricks.objects.filter(sub_topic=sub_topic).order_by('-pk')[:5]
	response.update({'tipsandtricks':tipsandtricks})
	readandlearn = OnewordQuestion.objects.filter(sub_topic=sub_topic).order_by('-pk')[:2]
	response.update({'readandlearn':readandlearn})
	return render_to_response('subtopic_content.html', response)
					






				

