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
import time

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import *
from pscexams.student.models import UserProfile
from pscexams.forum.models import Question, QuestionView, Tag, QuestionTag, Answer, Comment, QuestionVotes, AnswerVotes, Ad
from pscexams.sms import *

def admin_check(user):
	try:
		user_profile = UserProfile.objects.get(user=user)
	except:
		return False
	if user_profile.user_type == UserType.types['Admin']:
		return True
	else:
		return False

@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
	response = {}
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		raise Http500	
	
	response.update({'usertypes':UserType.types})

	response.update({'user_count':UserProfile.objects.all().count()})
	response.update({'activeuser_count':UserProfile.objects.filter(user__is_active = True).count()})

	if 'user_type' in request.GET and request.GET['user_type'] != '0':
		user_type = request.GET['user_type']
		users = UserProfile.objects.filter(user_type=user_type).order_by('-pk')[:20]
		response.update({'usertype_selected':True})
		response.update({'selected_usertype':user_type})

	else:
		users = UserProfile.objects.all().order_by('-pk')[:20]
	response.update({'users':users})
	return render_to_response('user_details.html', response)


# /siteadmin/users/ajax/browse/
def siteadmin_user_ajax_browse(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect(DefaultUrl.login_url)
	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		raise Http500

	if user_profile.user_type != UserType.types['Admin']:
		raise Http404()
	get_error = False

	if 'user_type' in request.GET and request.GET['user_type']:
		user_type = request.GET['user_type']		
	else:
		get_error = True	

	if 'next_rows' in request.GET and request.GET['next_rows']:
		next_rows = request.GET['next_rows']
	else:
		get_error = True

	if get_error:
		raise Http404

	next_row = int(next_rows)
	end_row = next_row + 20	

	if user_type == "undefined":
		users = UserProfile.objects.all().order_by('-pk')[next_row:end_row]
	else:
		users = UserProfile.objects.filter(user_type=user_type).order_by('-pk')[next_row:end_row]

	if not users:
		return HttpResponse('Null')
	else:
		return render_to_response('ajax_users.html', {'users':users})

#/siteadmin/ajax/users/search/
def siteadmin_ajax_users_search_username(request):
    if not request.user.is_authenticated():
        raise Http404        
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http500

    if user_profile.user_type != UserType.types['Admin']:
        raise Http404()
        
    if 'email' in request.GET and request.GET['email']:
        email = request.GET['email']
    else:
        raise Http404()        
    try:
        user = UserProfile.objects.get(user__username=email)
    except:
        return HttpResponse("False")
        
    response = {}
    response.update({'user':user})
    return render_to_response('ajax_particular_user.html', response)


@login_required
@user_passes_test(admin_check)
def user_workdetails(request):
	response = {}
	if 'user_id' in request.GET and request.GET['user_id']:
		user_id = request.GET['user_id']
	else:
		raise Http404()
		
	return HttpResponse(user_id)        
@login_required
@user_passes_test(admin_check)
def admin_add_exam(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})

	if request.method == 'GET':
		return render_to_response('add_exam.html', response)

	if request.method == 'POST':
		form_error = False
		if 'state' in request.POST and request.POST['state']:
			state = request.POST['state']
		else:
			form_error = True

		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']
		else:
			form_error = True

		if 'image_url' in request.POST and request.POST['image_url']:
			image_url = request.POST['image_url']
		else:
			image_url = " "

		if 'description' in request.POST and request.POST['description']:
			description = request.POST['description']
		else:
			form_error = True

		if form_error:
			response.update({'form_error':form_error})
			return render_to_response('add_exam.html', response) 

		exam = Exam(state = get_object_or_404(State,id=state), exam = exam, image = image_url)
		exam.save()
		examdescription = ExamDescription(exam = get_object_or_404(Exam,id=exam.id), description = description)
		try:
			examdescription.save()
			response.update({'saved':True})
		except:
			response.update({'save_error':True})

		return render_to_response('add_exam.html', response)


@login_required
@user_passes_test(admin_check)
def admin_add_subject(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})

	if request.method == 'GET':
		return render_to_response('add_subject.html', response)

	if request.method == 'POST':
		form_error = False
		if 'state' in request.POST and request.POST['state']:
			state = request.POST['state']
		else:
			form_error = True

		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']
		else:
			form_error = True

		if 'subject' in request.POST and request.POST['subject']:
			subject = request.POST['subject']
		else:
			form_error = True

		if form_error:
			response.update({'form_error':form_error})
			return render_to_response('add_subject.html', response) 

		subject = Subject(state = get_object_or_404(State,id=state), exam = get_object_or_404(Exam,id=exam), subject = subject)
		try:
			subject.save()
			response.update({'saved':True})
		except:
			response.update({'save_error':True})

		return render_to_response('add_subject.html', response)


@login_required
@user_passes_test(admin_check)
def admin_add_topic(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})

	if request.method == 'GET':
		return render_to_response('add_topic.html', response)

	if request.method == 'POST':
		form_error = False
		if 'state' in request.POST and request.POST['state']:
			state = request.POST['state']
		else:
			form_error = True

		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']
		else:
			form_error = True

		if 'subject' in request.POST and request.POST['subject']:
			subject = request.POST['subject']
		else:
			form_error = True

		if 'topic' in request.POST and request.POST['topic']:
			topic = request.POST['topic']
		else:
			form_error = True

		if form_error:
			response.update({'form_error':form_error})
			return render_to_response('add_topic.html', response) 

		topic = Topic(state = get_object_or_404(State,id=state), exam = get_object_or_404(Exam,id=exam), subject = get_object_or_404(Subject,id=subject), topic = topic)
		try:
			topic.save()
			response.update({'saved':True})
		except:
			response.update({'save_error':True})

		return render_to_response('add_topic.html', response)


@login_required
@user_passes_test(admin_check)
def admin_add_sub_topic(request):
	response = {}
	states = State.objects.all()
	response.update({'states':states})

	if request.method == 'GET':
		return render_to_response('add_sub_topic.html', response)

	if request.method == 'POST':
		form_error = False
		if 'state' in request.POST and request.POST['state']:
			state = request.POST['state']
		else:
			form_error = True

		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']
		else:
			form_error = True

		if 'subject' in request.POST and request.POST['subject']:
			subject = request.POST['subject']
		else:
			form_error = True

		if 'topic' in request.POST and request.POST['topic']:
			topic = request.POST['topic']
		else:
			form_error = True

		if 'sub_topic' in request.POST and request.POST['sub_topic']:
			sub_topic = request.POST['sub_topic']
		else:
			form_error = True

		if 'description' in request.POST and request.POST['description']:
			description = request.POST['description']
		else:
			form_error = True

		if form_error:
			response.update({'form_error':form_error})
			return render_to_response('add_sub_topic.html', response) 

		sub_topic = SubTopic(state = get_object_or_404(State,id=state), exam = get_object_or_404(Exam,id=exam), subject = get_object_or_404(Subject,id=subject), topic = get_object_or_404(Topic,id=topic), sub_topic = sub_topic, descripition = description)
		try:
			sub_topic.save()
			response.update({'saved':True})
		except:
			response.update({'save_error':True})

		return render_to_response('add_sub_topic.html', response)


@login_required
@user_passes_test(admin_check)
def admin_upload_modelexamquestion(request):
	response = {}
	modelexams = ModelExam.objects.all()
	response.update({'modelexams':modelexams})
	
	if request.method == 'GET':
		return render_to_response('modelexam_questionpaper.html', response)

	if request.method == 'POST':
   
	    if 'model_exam' in request.POST and request.POST['model_exam']:
	        model_exam = request.POST['model_exam']
	    
	    try:
	        model_exam = ModelExam.objects.get(id=model_exam)
	    except:
	        raise Http404()   

	    if 'question_url' in request.FILES and request.FILES:
	    	question_url = request.FILES['question_url']
	    	question_file = request.FILES['question_url'].name
	    	question_file_extension = os.path.splitext(question_file)[1]
	    	new_question_file = str(model_exam.pk) + 'ques' + str(datetime.datetime.now().strftime("%b%d%Y%H%M%S"))
	    	
	    	try:
	    		f1 = open('/tmp/'+ new_question_file + question_file_extension,'wb+')
	    		for chunk in question_url.chunks():
	    			f1.write(chunk)
	    		f1.close()
	    	except:
	    		raise Http404()
	    	
	    	try:
	    		# Copy to Amazon.
	    		conn = S3Connection('AKIAJTA3FH3TQEMQ25HA', 'YLBDeel7NLEOoM+leAXWy7hby3m4Dh4kU1g4CaUF') # DO NOT LOOSE THIS KEY!!!!!
	    		bucket = conn.create_bucket('questionpapers.smartindia')
	    		k = Key(bucket)
	    		k.key = new_question_file + question_file_extension
	    		k.set_contents_from_filename('/tmp/' + new_question_file + question_file_extension)
	    		k.set_acl('public-read')
	    	except:
	    		raise Http404()

	    if 'answer_url' in request.FILES and request.FILES:
	    	answer_url = request.FILES['answer_url']
	    	answer_file = request.FILES['answer_url'].name
	    	answer_file_extension = os.path.splitext(answer_file)[1]
	    	new_answer_file = str(model_exam.pk) + 'ans' + str(datetime.datetime.now().strftime("%b%d%Y%H%M%S"))

	    	try:
	    		f2 = open('/tmp/'+ new_answer_file + answer_file_extension,'wb+')
	    		for chunk in answer_url.chunks():
	    			f2.write(chunk)
	    		f2.close()
	    	except:
	    		raise Http404()

	    	try:
	    		# Copy to Amazon.
	    		conn = S3Connection('AKIAJTA3FH3TQEMQ25HA', 'YLBDeel7NLEOoM+leAXWy7hby3m4Dh4kU1g4CaUF') # DO NOT LOOSE THIS KEY!!!!!
	    		bucket = conn.create_bucket('questionpapers.smartindia')
	    		k = Key(bucket)
	    		k.key = new_answer_file + answer_file_extension
	    		k.set_contents_from_filename('/tmp/' + new_answer_file + answer_file_extension)
	    		k.set_acl('public-read')
	    	except:
	    		raise Http404()
	    try:
	    	model_question_paper = ModelExamQuestionPaper()	    	
	    	model_question_paper.modelexam = model_exam
	    	model_question_paper.question_path = '/tmp/' + new_question_file + question_file_extension
	    	model_question_paper.answer_path = '/tmp/'+ new_answer_file + answer_file_extension
	    	model_question_paper.question_url = 'https://s3.amazonaws.com/questionpapers.smartindia/' + new_question_file + question_file_extension
	    	model_question_paper.answer_url = 'https://s3.amazonaws.com/questionpapers.smartindia/' + new_answer_file + answer_file_extension
	    	model_question_paper.save()
	    except:
	    	raise Http404()

	    response.update({'saved':True})
	    return render_to_response('modelexam_questionpaper.html',response)


@login_required
@user_passes_test(admin_check)
def admin_upload_previousyearquestion(request):
	response = {}
	exams = Exam.objects.all()
	response.update({'exams':exams})
	
	if request.method == 'GET':
		return render_to_response('previousyear_questionpaper.html', response)

	if request.method == 'POST':
		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']

		if 'title' in request.POST and request.POST['title']:
			title = request.POST['title']

		try:
			exam_obj = Exam.objects.get(id=exam)
		except:
			raise Http404()

		if 'question_url' in request.FILES and request.FILES:
			question_url = request.FILES['question_url']
			question_file = request.FILES['question_url'].name
			question_file_extension = os.path.splitext(question_file)[1]
			new_question_file = str(exam_obj.pk) + 'ques' + str(datetime.datetime.now().strftime("%b%d%Y%H%M%S"))

			try:
				f1 = open('/tmp/'+ new_question_file + question_file_extension,'wb+')
				for chunk in question_url.chunks():
					f1.write(chunk)
				f1.close()
			except:
				raise Http404()

			try:
				conn = S3Connection('AKIAJTA3FH3TQEMQ25HA', 'YLBDeel7NLEOoM+leAXWy7hby3m4Dh4kU1g4CaUF') # DO NOT LOOSE THIS KEY!!!!!
				bucket = conn.create_bucket('questionpapers.smartindia')
				k = Key(bucket)
				k.key = new_question_file + question_file_extension
				k.set_contents_from_filename('/tmp/' + new_question_file + question_file_extension)
				k.set_acl('public-read')
			except:
				raise Http404()

		if 'answer_url' in request.FILES and request.FILES:
			answer_url = request.FILES['answer_url']
			answer_file = request.FILES['answer_url'].name
			answer_file_extension = os.path.splitext(answer_file)[1]
			new_answer_file = str(exam_obj.pk) + 'ans' + str(datetime.datetime.now().strftime("%b%d%Y%H%M%S"))

			try:
				f2 = open('/tmp/'+ new_answer_file + answer_file_extension,'wb+')
				for chunk in answer_url.chunks():
					f2.write(chunk)
				f2.close()
			except:
				raise Http404()

			try:
				conn = S3Connection('AKIAJTA3FH3TQEMQ25HA', 'YLBDeel7NLEOoM+leAXWy7hby3m4Dh4kU1g4CaUF') # DO NOT LOOSE THIS KEY!!!!!
				bucket = conn.create_bucket('questionpapers.smartindia')
				k = Key(bucket)
				k.key = new_answer_file + answer_file_extension
				k.set_contents_from_filename('/tmp/' + new_answer_file + answer_file_extension)
				k.set_acl('public-read')
			except:
				raise Http404()

		try:
			previousyear_question_paper = PreviousYearQuestionPaper()
			previousyear_question_paper.exam = exam_obj
			previousyear_question_paper.name = title
			previousyear_question_paper.question_path = '/tmp/' + new_question_file + question_file_extension
			previousyear_question_paper.answer_path = '/tmp/'+ new_answer_file + answer_file_extension
			previousyear_question_paper.question_url = 'https://s3.amazonaws.com/questionpapers.smartindia/' + new_question_file + question_file_extension
			previousyear_question_paper.answer_url = 'https://s3.amazonaws.com/questionpapers.smartindia/' + new_answer_file + answer_file_extension
			previousyear_question_paper.save()
			response.update({'saved':True})
		except:
			raise Http404()

		return render_to_response('previousyear_questionpaper.html',response)

@login_required
@user_passes_test(admin_check)
def questions(request):
	response = {}
	questions = Question.objects.filter(approved=False)
	response.update({'questions':questions})
	return render_to_response('forum/siteadmin/question.html', response)

@login_required
@user_passes_test(admin_check)
def answers(request):
	response = {}
	answers = Answer.objects.filter(approved=False)
	response.update({'answers':answers})
	return render_to_response('forum/siteadmin/answer.html', response)

@login_required
@user_passes_test(admin_check)
def comments(request):
	response = {}
	comments = Comment.objects.filter(approved=False)
	response.update({'comments':comments})
	return render_to_response('forum/siteadmin/comment.html', response)

@login_required
@user_passes_test(admin_check)
def approve_question(request):
	response = {}
	if 'question' in request.GET and request.GET['question']:
		question_id = request.GET['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, id=question_id)
	question.approved = True
	question.save()

	return HttpResponse('ok')

@login_required
@user_passes_test(admin_check)
def delete_question(request):
	response = {}

	if 'question' in request.GET and request.GET['question']:
		question_id = request.GET['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, id=question_id)
	question.delete()

	return HttpResponse('ok')

@login_required
@user_passes_test(admin_check)
def approve_answer(request):
	response = {}

	if 'answer' in request.GET and request.GET['answer']:
		answer_id = request.GET['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, id=answer_id)
	answer.approved = True
	answer.save()
	answer.question.save()

	return HttpResponse('ok')

@login_required
@user_passes_test(admin_check)
def delete_answer(request):
	response = {}

	if 'answer' in request.GET and request.GET['answer']:
		answer_id = request.GET['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, id=answer_id)
	answer.delete()

	return HttpResponse('ok')

@login_required
@user_passes_test(admin_check)
def approve_comment(request):
	response = {}

	if 'comment' in request.GET and request.GET['comment']:
		comment_id = request.GET['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, id=comment_id)
	comment.approved = True
	comment.save()

	return HttpResponse('ok')

@login_required
@user_passes_test(admin_check)
def delete_comment(request):
	response = {}

	if 'comment' in request.GET and request.GET['comment']:
		comment_id = request.GET['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, id=comment_id)
	comment.delete()

	return HttpResponse('ok')


@login_required
@user_passes_test(admin_check)
def send_message(request):
	response = {}
	response.update(csrf(request))
	if request.method == 'GET':
		return render_to_response('send_sms.html')

	if 'message' in request.POST and request.POST['message']:
		message = request.POST['message']
	else:
		response.update({'message_error':True})
		return render_to_response('send_sms.html', response)

	students = UserProfile.objects.filter(user_type=UserType.types['Student'])
	for student in students:
		send_sms(message, str(student.mobile_no))
		time.sleep(5)

	response.update({'success':True})
	return render_to_response('send_sms.html', response)

# Details of User
#/siteadmin/user/details/
@login_required
@user_passes_test(admin_check)
def user_details(request, pk):
	response = {}
	user = get_object_or_404(User, pk=pk)
	response.update({'student':user})
	user_profile = get_object_or_404(UserProfile, user=user)
	response.update({'user_profile':user_profile})
	response.update({'usertypes':UserType.types})
	return render_to_response('user_registration_details.html', response)

