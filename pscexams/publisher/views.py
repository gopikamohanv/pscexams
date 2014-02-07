from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import *
from pscexams.student.models import UserProfile


def publisher_check(user):
	try:
		user_profile = get_object_or_404(UserProfile, user=user)
	except:
		return False
	if user_profile.user_type == UserType.types['Publisher']:
		return True
	else:
		return False


@login_required
@user_passes_test(publisher_check)
def publisher_dashboard(request):
	response = {}
	response.update({'user':request.user})
	response.update({'states':State.objects.all()})
	return render_to_response('publisher_home.html', response)


@login_required
@user_passes_test(publisher_check)
def publisher_create_modelexam(request):
	response = {}
	response.update({'user':request.user})
	response.update({'exams':Exam.objects.all()})

	if request.method == 'GET':
		return render_to_response('create_modelexam.html', response)

	if request.method == 'POST':
		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']
		
		if 'title' in request.POST and request.POST['title']:
			title = request.POST['title']
		
		if 'max_question' in request.POST and request.POST['max_question']:
			max_question = request.POST['max_question']
		
		if 'max_time' in request.POST and request.POST['max_time']:
			max_time = request.POST['max_time']

		model_exam = ModelExam()
		model_exam.title = title
		model_exam.exam = get_object_or_404(Exam, id=exam)
		model_exam.max_question = max_question
		model_exam.max_time = max_time
		try:
			model_exam.save()
			response.update({'success':True})
		except:
			response.update({'form_error':True})
			response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
			return render_to_response('create_modelexam.html', response)

		return render_to_response('create_modelexam.html', response)


@login_required
@user_passes_test(publisher_check)
def publisher_select_modelexam_questions(request):
	response = {}
	response.update({'user':request.user})
	exams = Exam.objects.all()
	response.update({'exams':exams})
	modelexams = ModelExam.objects.all()
	response.update({'modelexams':modelexams})
	return render_to_response('select_modelexam_questions.html', response)


@login_required
@user_passes_test(publisher_check)
def modelexam_ajax_question(request):
	response = {}
	if 'exam' in request.GET and request.GET['exam']:
		exam = request.GET['exam']
	try:
		modelexams = ModelExam.objects.filter(exam=exam)
		response.update({'modelexams':modelexams})
	except:
		response.update({'no_questions':True})
	return render_to_response('ajax_select_modelexam.html', response)


@login_required
@user_passes_test(publisher_check)
def publisher_add_modelexam_questions(request):
	response = {}

	if request.method == 'GET':
		if 'test' in request.GET and request.GET['test']:
			test = request.GET['test']

		if 'exam' in request.GET and request.GET['exam']:
			exam = request.GET['exam']

		subjects = Subject.objects.filter(exam=exam)
		response.update({'subjects':subjects})
		#return HttpResponse(subjects)
		response.update({'test':test})
		return render_to_response('add_questions.html', response)

	if request.method == 'POST':
		if 'test' in request.POST and request.POST['test']:
			test = request.POST['test']

		if 'count' in request.POST and request.POST['count']:
			count = int(request.POST['count'])
        else:
            count = 0
        
        test_obj = get_object_or_404(ModelExam, id=test)

        i = 1
        modelexam_question = ""
        while i <= count:
            question = "question_" + str(i)
            if question in request.POST and request.POST[question]:
                qn = request.POST[question]

                try:
                    qn_obj = Question.objects.get(pk=qn)
                except:
                    raise Http404("question didnt get")

                try:
                	modelexam_question = ModelExamQuestion.objects.get(modelexam = test_obj, question = qn_obj)
                except:
                	pass

                if not modelexam_question:
	                modelexam_question = ModelExamQuestion()
	                modelexam_question.modelexam = test_obj
	                modelexam_question.question = qn_obj
	                try:
	                    modelexam_question.save()
	                except:
	                    response.update({'save_error':True})
            else:
                pass
            i = i + 1
        response.update({'question_saved':True})
        
        return render_to_response('add_questions.html', response)


# Ajax for tutor question search
# /subtopic/ajax/add/question/
def subtopic_ajax_add_question(request):
	response = {}
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	try:
		questions = Question.objects.filter(sub_topic=sub_topic)
		response.update({'questions':questions})
		count = questions.count()
		response.update({'count':count})
	except:
		response.update({'no_questions':True})
	return render_to_response('ajax_add_question.html', response)

