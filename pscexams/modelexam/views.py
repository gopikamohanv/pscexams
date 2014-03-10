from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import Exam, Question, Subject, Topic, SubTopic, OnewordQuestion, TipsandTricks, ModelExam, ModelExamQuestion, ModelExamQuestionPaper
from pscexams.student.models import UserProfile, MockTest, MockTestData, MockTestType, ExamTest, ExamScore

def student_check(user):
	try:
		user_profile = UserProfile.objects.get(user=user)
	except:
		return False
	if user_profile.user_type == UserType.types['Student']:
		return True
	else:
		return False

@login_required
@user_passes_test(student_check)
def student_modelexam(request,pk):
	response = {}
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exam':exam})
	response.update({'exams': Exam.objects.all()})
	response.update({'model_exams': ModelExam.objects.filter(exam=exam)})
	return render_to_response('student_modelexam.html', response)

@login_required
@user_passes_test(student_check)
def student_modelexam_start(request, pk):
	response = {}
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exam':exam})

	if 'id' in request.GET and request.GET['id']:
		modelexam_id = request.GET['id']
	else:
		response.update({'form_error':True})
		return render_to_response('modelexam_start.html', response)
	
	modelexam = get_object_or_404(ModelExam, pk=modelexam_id)
	response.update({'modelexam':modelexam})
	response.update({'exam_type': ExamType.types['ModelExam']})
	questions = ModelExamQuestion.objects.filter(modelexam=modelexam)
	if questions:
		response.update({'questions':questions})
		return render_to_response('modelexam_start.html', response)
	else:
		response.update({'form_error':True})
		return render_to_response('modelexam_start.html', response)

@login_required
@user_passes_test(student_check)
def student_modelexam_submit(request, pk):
	response = {}
	user = UserProfile.objects.get(user=request.user)
	response.update({'user':user})
	modelexam = get_object_or_404(ModelExam, pk=pk)

	if request.method == 'GET':
		return HttpResponseRedirect('/student/modelexam/start/' + pk + '/')

	if request.method == 'POST':
		if 'limit' in request.POST and request.POST['limit']:
			q_limit = int(request.POST['limit'])
		else:
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)
		if 'exam_type' in request.POST and request.POST['exam_type']:
			exam_type = request.POST['exam_type']
		else:
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)

		if 'exam' in request.POST and request.POST['exam']:
			exam = request.POST['exam']	
		else:
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)	

		if 'totalseconds' in request.POST and request.POST['totalseconds']:
			totalseconds = request.POST['totalseconds']
		else:
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)		

		exam_obj = get_object_or_404(Exam, pk=exam)
		response.update({'exam':exam_obj})
		# Data processing starts.............
		questions = {}
		answer = {}

		# Taking question from form and saving in dictionary
		form_error = False
		i = 1
		while i <= q_limit:
			q = 'q_' + str(i)
			if q in request.POST and request.POST[q]:
				questions.update({'q_'+str(i):request.POST[q]})
			else:
				form_error= True
			i = i + 1

		if form_error:
			return HttpResponse('a')
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)

		# Taking answers from form and saving in dictionary
		i = 1
		while i <= q_limit:
			a = 'answer_' + str(i)
			if a in request.POST and request.POST[a]:
				answer.update({'answer_'+str(i):request.POST[a]})
			else:
				answer.update({'answer_'+str(i):0})
			i = i + 1

		# Saving test data with time and score
		test = MockTest()
		try:
			user_profile = UserProfile.objects.get(user=request.user)
		except:
			return HttpResponse('b')
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)
		test.user = user_profile
		test.save()
		# Save the test data.
		correct_answers = 0
		unattended = 0

		i = 1
		while i <= q_limit:
			test_data = MockTestData()
			test_data.mock_test = test
			try:
				question = Question.objects.get(id=questions['q_' + str(i)])
			except:
				response.update({'form_error':True})
				return render_to_response('student_modelexam_complete.html', response)
			test_data.question = question
			test_data.answer = answer['answer_' + str(i)]
			if answer['answer_' + str(i)] == 0:
				test_data.answered = False
				unattended += 1
			else:
				test_data.answered = True
			test_data.save()
			if test_data.answer == question.answer:
				correct_answers += 1
			del(test_data)
			i = i + 1

		# Update the score
		total_score = int(q_limit)
		wrong_answers = int(total_score) - (int(correct_answers) + int(unattended))
		score = int(correct_answers) -(int(wrong_answers)/3)
		test.correct_answers = correct_answers
		test.score = score
		test.time_taken = totalseconds
		test.save()

		mock_test_type = MockTestType()
		if exam_type == ExamType.types['Practice']:
			mock_test_type.mock_test_type = ExamType.types['Practice']
		
		elif exam_type == ExamType.types['Exam']:
			mock_test_type.mock_test_type = ExamType.types['Exam']
			
		elif exam_type == ExamType.types['ModelExam']:
			mock_test_type.mock_test_type = ExamType.types['ModelExam']	

		else:
			response.update({'form_error':True})
			return render_to_response('student_modelexam_complete.html', response)

		mock_test_type.mock_test = test
		mock_test_type.exam = pk

		try:
			ModelexamScore.objects.create(user=user, modelexam=modelexam, test=test)
		except:
			pass	
		
		response.update({'score':score})
		response.update({'total_score':total_score})
		response.update({'test':test})
		response.update({'success':True})
		response.update({'modelexams': ModelExam.objects.filter(exam=exam_obj)})
		
		# Time taken for the test
		response.update({'minutes':int(totalseconds) / 60})
		response.update({'seconds':int(totalseconds) % 60})
		return render_to_response('student_modelexam_complete.html', response)
	raise Http404()	


@login_required
@user_passes_test(student_check)
def student_modelexam_download(request, pk):
	response = {}
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	if 'id' in request.GET and request.GET['id']:
		modelexam_id = request.GET['id']
	else:
		response.update({'form_error':True})
		return render_to_response({'student_modelexam_download.html', response})
	modelexam = get_object_or_404(ModelExam, pk=modelexam_id)
	try:
		modelquestion = ModelExamQuestionPaper.objects.get(modelexam=modelexam)
		response.update({'modelquestion':modelquestion})
	except:
		response.update({'form_error': True})
	response.update({'exams':Exam.objects.all()})
	return render_to_response('student_modelexam_download.html', response)	

			





