from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import Exam, Question, Subject, Topic, SubTopic, OnewordQuestion
from pscexams.student.models import UserProfile, MockTest, MockTestData, MockTestType, ExamTest

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
def student_dashboard(request):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exams':Exam.objects.all()})
	return render_to_response('student_home.html', response)

@login_required
@user_passes_test(student_check)
def student_exam(request, pk):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	return render_to_response('student_subjects.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_subject(request, pk):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	subject = get_object_or_404(Subject, pk=pk)
	response.update({'subject':subject})
	if 'topic' in request.GET and request.GET['topic']:
		response.update({'topic_id':int(request.GET['topic'])})
	return render_to_response('student_topics.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_topic_tests(request, pk):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	sub_topic = get_object_or_404(SubTopic, pk=pk)
	tests = Question.objects.filter(sub_topic=sub_topic).count() / 10
	tests = range(1, tests+1)
	response.update({'sub_topic':sub_topic})
	response.update({'tests':tests})
	if 'locked' in request.GET and request.GET['locked']:
		response.update({'locked':True})
	if 'test' in request.GET and request.GET['test']:
		response.update({'test':request.GET['test']})
	mocktest_data = MockTestData.objects.filter(question__sub_topic=sub_topic).order_by('-pk')[:5]
	response.update({'mocktest_data':mocktest_data})
	response.update({'sub_topic':sub_topic})		 
	return render_to_response('student_topic_tests.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_topic(request, pk, test):
	response = {}
	test = int(test)
	user = UserProfile.objects.get(user=request.user)
	response.update({'user':user})
	sub_topic = get_object_or_404(SubTopic, pk=pk)
	response.update({'sub_topic':sub_topic})

	if test > 1:
		try:
			exam = ExamTest.objects.get(user=user, exam_topic=sub_topic)
		except:
			return HttpResponseRedirect('/student/exam/topic/tests/'+ str(pk) +'/?locked=true&test=1')	
		else:
			if not exam.test_num == test -1:
				return HttpResponseRedirect('/student/exam/topic/tests/'+ str(pk) +  '/?locked=true&test=' + str(exam.test_num + 1))	

	page = int(test) - 1
	questions = Question.objects.filter(sub_topic=sub_topic).order_by('pk')[(page*10):(page*10)+10]
	if questions.count() < 10:
		pass
	else:
		response.update({'questions':questions})
	response.update({'test':test})
	response.update({'exam_type':ExamType.types['Exam']})
	return render_to_response('student_exam.html', response)


@login_required
@user_passes_test(student_check)
def student_exam_submit(request, pk):
	response = {}
	user = UserProfile.objects.get(user=request.user)
	response.update({'user':user})

	try:
		sub_topic = get_object_or_404(SubTopic, pk=pk)
	except:
		raise Http404()

	if request.method == 'GET':
		return HttpResponseRedirect('/student/exam/topic/tests/' + pk + '/')

	if request.method == "POST":
		if 'limit' in request.POST and request.POST['limit']:
			q_limit = int(request.POST['limit'])
		else:
			response.update({'form_error':True})
			return render_to_response('student_exam_complete.html', response)

		if 'exam_type' in request.POST and request.POST['exam_type']:
			exam_type = request.POST['exam_type']
		else:
			response.update({'form_error':True})
			return render_to_response('student_exam_complete.html', response)

		if 'test' in request.POST and request.POST['test']:
			test_num = int(request.POST['test'])
		else:
			response.update({'form_error':True})
			return render_to_response('student_exam_complete.html', response)

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
			return render_to_response('student_exam_complete.html', response)

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
			return render_to_response('student_exam_complete.html', response)
		test.user = user_profile
		test.save()
		# Save the test data.
		correct_answers = 0

		i = 1
		while i <= q_limit:
			test_data = MockTestData()
			test_data.mock_test = test
			try:
				question = Question.objects.get(id=questions['q_' + str(i)])
			except:
				response.update({'form_error':True})
				return render_to_response('student_exam_complete.html', response)
			test_data.question = question
			test_data.answer = answer['answer_' + str(i)]
			if answer['answer_' + str(i)] == 0:
				test_data.answered = False
			else:
				test_data.answered = True
			test_data.save()
			if test_data.answer == question.answer:
				correct_answers += 1
			del(test_data)
			i = i + 1

		# Update the score
		total_score = int(q_limit)
		wrong_answers = int(q_limit) - int(correct_answers)
		score = (int(q_limit)) - (int(wrong_answers))
		test.correct_answers = correct_answers
		test.score = score
		test.save()

		mock_test_type = MockTestType()
		if exam_type == ExamType.types['Practice']:
			mock_test_type.mock_test_type = ExamType.types['Practice']
		
		elif exam_type == ExamType.types['Exam']:
			mock_test_type.mock_test_type = ExamType.types['Exam']
		else:
			response.update({'form_error':True})
			return render_to_response('student_exam_complete.html', response)

		mock_test_type.mock_test = test
		mock_test_type.exam = pk

		try:
			sub_topic = SubTopic.objects.get(pk=pk)
			response.update({'sub_topic':sub_topic})
		except:
			pass

		if int(wrong_answers) == 0:
			try:
				exam = ExamTest.objects.get(user=user, exam_topic=sub_topic)
			except:
				ExamTest.objects.create(user=user, exam_topic=sub_topic, test_num=test_num)
			else:
				exam.test_num = test_num
				exam.save()

		response.update({'score':score})
		response.update({'total_score':total_score})
		response.update({'test':test})
		response.update({'success':True})
		return render_to_response('student_exam_complete.html', response)

	raise Http404()

@login_required
@user_passes_test(student_check)
def student_answersheets_list(request):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	return render_to_response('student_answersheets_list.html', response)

@login_required
@user_passes_test(student_check)
def student_answersheet(request, pk):
	response = {}
	test_data = get_object_or_404(MockTest, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'test':test_data})
	response.update({'total_score': test_data.mocktestdata_set.count()})
	return render_to_response('student_answersheet.html', response)

@login_required
@user_passes_test(student_check)
def student_onewords(request,pk):
	response = {}
	topic = get_object_or_404(Topic, pk=pk)
	response.update({'topic':topic})
	response.update({'sub_topics': SubTopic.objects.filter(topic=topic)})
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	else:
		response.update({'form_error': True})
		return render_to_response('student_onewords.html', response)
	sub_topic_obj = get_object_or_404(SubTopic,pk=sub_topic)
	response.update({'sub_topic':sub_topic_obj})			
	onewords = OnewordQuestion.objects.filter(sub_topic=sub_topic)
	response.update({'onewords':onewords})			
	return render_to_response('student_onewords.html', response)






