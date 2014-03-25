from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib import auth

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import Exam, Question, Subject, Topic, SubTopic, OnewordQuestion, TipsandTricks, State, PreviousYearQuestionPaper
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
def student_dashboard(request):
	response = {}
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exams':Exam.objects.all()})
	response.update({'oneword':OnewordQuestion.objects.all().order_by('-pk')[:2]})
	response.update({'tricks':TipsandTricks.objects.all().order_by('-pk')[:2]})
	return render_to_response('student_home.html', response)

@login_required
@user_passes_test(student_check)
def student_exam(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	return render_to_response('student_subjects.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_subject(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
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
	response.update({'exams':Exam.objects.all()})
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
	related_exams = ExamScore.objects.filter(sub_topic=sub_topic).order_by('-pk')[:10]
	response.update({'related_exams':related_exams})		 
	return render_to_response('student_topic_tests.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_topic(request, pk, test):
	response = {}
	response.update({'exams':Exam.objects.all()})
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
			if test > exam.test_num:
				if not test == exam.test_num + 1:
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
	response.update({'exams':Exam.objects.all()})
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
		try:
			ExamScore.objects.create(user=user, sub_topic=sub_topic, test=test)
		except:
			pass	
		
		response.update({'score':score})
		response.update({'total_score':total_score})
		response.update({'test':test})
		response.update({'success':True})
		related_exams = ExamScore.objects.filter(sub_topic=sub_topic).order_by('-pk')[:10]
		response.update({'related_exams':related_exams})
		response.update({'sub_topic':sub_topic})
		return render_to_response('student_exam_complete.html', response)

	raise Http404()

@login_required
@user_passes_test(student_check)
def student_answersheets_list(request):
	response = {}
	response.update({'exams':Exam.objects.all()})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	related_exams = ExamScore.objects.filter(sub_topic=sub_topic).order_by('-pk')
	response.update({'related_exams':related_exams})
	sub_topic_name = SubTopic.objects.get(id=sub_topic)
	response.update({'sub_topic_name':sub_topic_name})
	response.update({'sub_topic':sub_topic})
	return render_to_response('student_answersheets_list.html', response)

@login_required
@user_passes_test(student_check)
def student_answersheet(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	test_data = get_object_or_404(MockTest, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'test':test_data})
	response.update({'total_score': test_data.mocktestdata_set.count()})
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	related_exams = ExamScore.objects.filter(sub_topic=sub_topic).order_by('-pk')[:10]
	response.update({'related_exams':related_exams})
	response.update({'sub_topic':sub_topic})
	return render_to_response('student_answersheet.html', response)

@login_required
@user_passes_test(student_check)
def student_onewords(request,pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	topic = get_object_or_404(Topic, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exams':Exam.objects.all()})
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

@login_required
@user_passes_test(student_check)
def student_tips_topics(request,pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	topic = get_object_or_404(Topic, pk=pk)
	response.update({'topic':topic})
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']
	else:
		response.update({'form_error': True}) 
		return render_to_response('tips_topics.html', response)
	sub_topic_obj = get_object_or_404(SubTopic,pk=sub_topic)
	response.update({'sub_topic':sub_topic_obj})
	tips = TipsandTricks.objects.filter(sub_topic=sub_topic_obj)
	if tips:
		response.update({'tips': tips})
	else:
		response.update({'no_tips':True})		
	return render_to_response('tips_topics.html', response)

@login_required
@user_passes_test(student_check)
def student_tips_view(request, pk):
	response = 	{}
	response.update({'exams':Exam.objects.all()})
	sub_topic = get_object_or_404(SubTopic, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'sub_topic':sub_topic})
	if 'id' in request.GET and request.GET['id']:
		tip_id = request.GET['id']
	else:
		response.update({'no_tips': True})
		return render_to_response('tips_view.html', response)

	tip = get_object_or_404(TipsandTricks, pk=int(tip_id))
	response.update({'tip':tip})
	return render_to_response('tips_view.html', response)

@login_required
@user_passes_test(student_check)
def student_question_new(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	sub_topic = get_object_or_404(SubTopic, pk=pk)
	response.update({'sub_topic':sub_topic})
	if 'id' in request.GET and request.GET['id']:
		oneword_id = request.GET['id']
	else:
		response.update({'form_error':True})
		return render_to_response('new_oneword.html', response)	
	response.update({'oneword': OnewordQuestion.objects.get(id=oneword_id)})
	response.update({'onewords': OnewordQuestion.objects.filter(sub_topic=sub_topic).order_by('?')[:8]})
	return render_to_response('new_oneword.html', response)

@login_required
@user_passes_test(student_check)
def student_trick_new(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	sub_topic = get_object_or_404(SubTopic, pk=pk)
	response.update({'sub_topic':sub_topic})

	if 'id' in request.GET and request.GET['id']:
		trick_id = request.GET['id']
	else:
		response.update({'form_error': True})
		return render_to_response('new_trick.html', response)
	response.update({'trick': TipsandTricks.objects.get(id=trick_id)})
	response.update({'tricks': TipsandTricks.objects.filter(sub_topic=sub_topic).order_by('?')[:5]})
	return render_to_response('new_tricks.html', response)	

@login_required
@user_passes_test(student_check)
def student_performance(request, pk):
	response = {}
	exam = get_object_or_404(Exam, pk=pk)
	user = get_object_or_404(UserProfile, user=request.user)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exam':exam})
	response.update({'user':UserProfile.objects.get(user=request.user)})
	scores = ExamScore.objects.filter(user=user, sub_topic__exam=exam).order_by('-pk')[:10]
	if scores:
		response.update({'scores': scores})
	else:
		response.update({'no_tests':True})
	response.update({'subjects': Subject.objects.filter(exam=exam)})
	response.update({'exams': Exam.objects.all()})		
	return render_to_response('performance.html', response)


@login_required
@user_passes_test(student_check)
def student_profile(request):
	response = {}
	response.update(csrf(request))
	response.update({'user':UserProfile.objects.get(user=request.user)})
	response.update({'exams':Exam.objects.all()})

	if request.method == 'GET':
		return render_to_response('my_profile.html', response)

	if request.method == 'POST':
		form_error = False
		if 'first_name' in request.POST and request.POST['first_name']:
			first_name = request.POST['first_name']
		else:
			form_error = True

		
		if 'last_name' in request.POST and request.POST['last_name']:
			last_name = request.POST['last_name']
		else:
			last_name=''

		if 'email' in request.POST and request.POST['email']:
			email = request.POST['email']
		else:
			form_error = True

		
		if 'mobile' in request.POST and request.POST['mobile']:
			mobile = request.POST['mobile']
		else:
			mobile=''

		if form_error:
			response.update({'form_error':True})
			return render_to_response('my_profile.html', response)

		request.user.first_name = first_name
		request.user.last_name = last_name
		request.user.email = email
		request.user.save()
		try:
			userprofile = UserProfile.objects.get(user=request.user)
		except:
			raise Http404()
		else:
			userprofile.mobile_no = mobile
			userprofile.save()

		response.update({'success':True})
		response.update({'user':UserProfile.objects.get(user=request.user)})
		return render_to_response('my_profile.html', response)


@login_required
@user_passes_test(student_check)
def student_password_reset(request):
	response = {}
	response.update(csrf(request))
	response.update({'exams':Exam.objects.all()})

	if request.method == 'GET':
		return render_to_response('password_reset.html', response)

	if request.method == 'POST':
		form_error=False
		if 'current_password' in request.POST and request.POST['current_password']:
			current_password = request.POST['current_password']
		else:
			form_error = True

		if 'new_password' in request.POST and request.POST['new_password']:
			new_password = request.POST['new_password']
		else:
			form_error = True

		if 'confirm_password' in request.POST and request.POST['confirm_password']:
			confirm_password = request.POST['confirm_password']
		else:
			form_error = True

		if form_error:
			response.update({'form_error':True})
			return render_to_response('password_reset.html', response)

		user = auth.authenticate(username=request.user.username, password=current_password)
		if user is not None and user.is_active:
			pass
		else:
			response.update({'current_password_error':True})
			return render_to_response('password_reset.html', response)

		if not new_password == confirm_password:
			response.update({'password_error':True})
			return render_to_response('password_reset.html', response)

		request.user.set_password(confirm_password)
		request.user.save()
		response.update({'success':True})
		return render_to_response('password_reset.html', response)

def student_previous_year_exam(request, pk):
	response = {}
	response.update({'exams':Exam.objects.all()})
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'exam':exam})
	previous_exams = PreviousYearQuestionPaper.objects.filter(exam=exam)
	response.update({'previous_exams':previous_exams})
	return render_to_response('student_previous_year_download.html', response)