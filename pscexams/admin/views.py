from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os.path
import datetime

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import *
from pscexams.student.models import UserProfile


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
	user_details = UserProfile.objects.filter(user_type ='4')
	
	user_count = user_details.count()
	response.update({'user_details':user_details})
	response.update({'user':request.user})
	response.update({'user_count':user_count})
	return render_to_response('admin_home.html', response)


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

	if request.method == ' POST':
		return HttpResponse('fndsf')
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