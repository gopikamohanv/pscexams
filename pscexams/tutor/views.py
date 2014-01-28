from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib import auth

from pscexams.user_type import UserType
from pscexams.student.models import *
from pscexams.admin.models import *


# Pagination limit
PAGE_LIMIT = 3


# Add a new question for the tutor
# /tutor/questions/add/
def tutor_questions_add(request):
    response = {}
    response.update(csrf(request))

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http500

    response.update({'user':user_profile})

    if user_profile.user_type != UserType.types['Tutor']:
        return HttpResponseRedirect(DefaultUrl.login_url)

    
    states = State.objects.all()
    response.update({'states':states})

    if request.method == 'GET':
        # Check and load the default editor of the user
        return render_to_response('tutor_question_add.html', response)

    # Here comes a question save...
    form_error = False
    error_text = ''

    if 'state' in request.POST and request.POST['state']:
        state = request.POST['state']
        if state == '0':
            form_error = True
    else:
        form_error = True

    if 'exam' in request.POST and request.POST['exam']:
        exam = request.POST['exam']
        if exam == '0':
            form_error = True
    else:
        form_error = True

    if 'subject' in request.POST and request.POST['subject']:
        subject = request.POST['subject']
        if subject == '0':
            form_error = True
    else:
        form_error = True

    if 'topic' in request.POST and request.POST['topic']:
       topic  = request.POST['topic']
       if topic == '0':
           form_error = True
    else:
        form_error = True

    #TODO: Create a Config class for tutor and put difficulty levels in that class
    if 'test_type' in request.POST and request.POST['test_type']:
        test_type = request.POST['test_type']
        if test_type == '0':
            form_error = True
    else:
        form_error = True


    if 'question' in request.POST and request.POST['question']:
        question = request.POST['question']
    else:
        form_error = True

    if 'option1' in request.POST and request.POST['option1']:
        option1 = request.POST['option1']
    else:
        form_error = True

    if 'option2' in request.POST and request.POST['option2']:
        option2 = request.POST['option2']
    else:
        form_error = True

    if 'option3' in request.POST and request.POST['option3']:
        option3 = request.POST['option3']
    else:
        form_error = True

    if 'option4' in request.POST and request.POST['option4']:
        option4 = request.POST['option4']
    else:
        form_error = True

    if 'explanation' in request.POST and request.POST['explanation']:
        explanation = request.POST['explanation']
    else:
        form_error = True
        
    if 'answer_in_option' in request.POST and request.POST['answer_in_option']:
        answer_in_option = request.POST['answer_in_option']
    else:
        form_error = True

    
    if form_error:
        response.update({'form_error':True})
        response.update({'error_text':'Error: Please enter all required fields'})
        return render_to_response('tutor_question_add.html', response)

    # Get syllabus, grade, subject, chapter object before saving
    # We will make this a library in the future
    data_error = False
    try:
        topic_obj = Topics.objects.get(id=topic)
    except:
        data_error = True

    if data_error:
        response.update({'form_error':True})
        response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
        return render_to_response('tutor_question_add.html', response)

    # Create a new object and save the damn question
    question_obj = Question()
    question_obj.question = question
    question_obj.option1 = option1
    question_obj.option2 = option2
    question_obj.option3 = option3
    question_obj.option4 = option4
    question_obj.answer = answer_in_option
    question_obj.explanation = explanation
    question_obj.tutor = request.user
    question_obj.is_published = False
    question_obj.topic = topic_obj
    question_obj.mode = test_type
    question_obj.is_in_use = True
    # TODO: Add a try catch statement here
    try:
        question_obj.save()
    except:
        response.update({'form_error':True})
        response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
        return render_to_response('tutor_question_add.html', response)
    
   
    response.update({'question_saved':True})
    return render_to_response('tutor_question_add.html', response)


# Edit and save question for the tutor
# /tutor/questions/edit/
def tutor_questions_edit(request):
    response = {}
    response.update(csrf(request))

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http500

    if user_profile.user_type != UserType.types['Tutor']:
        return HttpResponseRedirect(DefaultUrl.login_url)



    if request.method == 'GET':
    	
    	states = State.objects.all()
    	response.update({'states':states})
    	if 'id' in request.GET and request.GET['id']:
            question_id = request.GET['id']
    	else:
        	response.update({'error':True})
        	return render_to_response('tutor_home.html', response)
        try:
        	question_obj = Question.objects.get(id=question_id)
    	except:
        	return Http404()
        response.update({'question_obj':question_obj})
        exams = Exam.objects.filter(state=question_obj.topic.state)
        subjects = Subject.objects.filter(exam=question_obj.topic.exam)
        topics = Topics.objects.filter(subject=question_obj.topic.subject)
        response.update({'exams':exams})
        response.update({'subjects':subjects})
        response.update({'topics':topics})
        return render_to_response('tutor_questions_edit.html', response)


    if request.method == 'POST':
    	states = State.objects.all()
    	response.update({'states':states})

   		
    	if 'question_id' in request.POST and request.POST['question_id']:
    		question_id = request.POST['question_id']
    	else:
    		response.update({'error':True})
    		return render_to_response('tutor_home.html', response)
    	
    	try:
    		question_obj = Question.objects.get(id=question_id)
    	except:
    		return Http404()

        form_error = False

    	if 'state' in request.POST and request.POST['state']:
    		state = request.POST['state']
    		if state == '0':
    			form_error = True
    	else:
    		form_error = True

    	if 'exam' in request.POST and request.POST['exam']:
    		exam = request.POST['exam']
    		if exam == '0':
    			form_error = True
    	else:
    		form_error = True

    	if 'subject' in request.POST and request.POST['subject']:
    		subject = request.POST['subject']
    		if subject == '0':
    			form_error = True
    	else:
    		form_error = True

    	if 'topic' in request.POST and request.POST['topic']:
    		topic = request.POST['topic']
    		if topic == '0':
    			form_error = True
    	else:
    		form_error = True

    	if 'test_type' in request.POST and request.POST['test_type']:
    		test_type = request.POST['test_type']
    		if test_type == '0':
    			form_error = True
    	else:
    		form_error = True

    	if 'question' in request.POST and request.POST['question']:
    		question = request.POST['question']
    	else:
    		form_error = True

    	if 'option1' in request.POST and request.POST['option1']:
    		option1 = request.POST['option1']
    	else:
    		form_error = True

    	if 'option2' in request.POST and request.POST['option2']:
    		option2 = request.POST['option2']
    	else:
    		form_error = True

    	if 'option3' in request.POST and request.POST['option3']:
    		option3 = request.POST['option3']
    	else:
    		form_error = True

        if 'option4' in request.POST and request.POST['option4']:
            option4 = request.POST['option4']
        else:
            form_error = True

        if 'explanation' in request.POST and request.POST['explanation']:
            explanation = request.POST['explanation']
        else:
            form_error = True

        if 'answer_in_option' in request.POST and request.POST['answer_in_option']:
            answer_in_option = request.POST['answer_in_option']
        else:
            form_error = True

        if form_error:
            response.update({'form_error':True})
            response.update({'error_text':'Error: Please enter all required fields'})

        data_error = False

        try:
            topic_obj = Topics.objects.get(id=topic)
        except:
            data_error = True

        if data_error:
            response.update({'form_error':True})
            response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
            return render_to_response('tutor_questions_edit.html', response)

        question_obj.question = question
        question_obj.option1 = option1
        question_obj.option2 = option2
        question_obj.option3 = option3
        question_obj.option4 = option4
        question_obj.answer = answer_in_option
        question_obj.explanation = explanation
        question_obj.tutor = request.user
        question_obj.is_published = False
        question_obj.topic = topic_obj
        question_obj.mode = test_type
        question_obj.is_in_use = True


        try:
            question_obj.save()
            response.update({'question_saved':True})
        except:
            response.update({'form_error':True})
            response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
            return render_to_response('tutor_questions_edit.html', response)

        states = State.objects.all()
        response.update({'states':states})
        response.update({'question_obj':question_obj})
        exams = Exam.objects.filter(state=question_obj.topic.state)
        subjects = Subject.objects.filter(exam=question_obj.topic.exam)
        topics = Topics.objects.filter(subject=question_obj.topic.subject)
        response.update({'exams':exams})
        response.update({'subjects':subjects})
        response.update({'topics':topics})
        return render_to_response('tutor_questions_edit.html', response)


# For Pagination
#/questions/browse/
def question_browse(request, page):
	response = {}
	response.update(csrf(request))
	response.update({'user':request.user})
	

	if 'page' in request.GET and request.GET['page']:
		page = int(request.GET['page'])
		response.update({'current_page':page})
	else:
		raise Http404()

	questions = Question.objects.filter(tutor=request.user)

	counter = page * 3
	pages = int(math.ceil(float(questions.count())/20)) 
	if page > pages:
		raise Http404()

	last = pages - 1
	if pages <= 5:
		pages = range(0,pages)
		count = 0
	else:
		if page <= 2:
			pages = range(0,5)
			count = 4
		else:
			if page == last or page == last - 1 :
				pages = range(page - 2 , pages)
				count = last + 1
			else:
				pages = range(page - 2, page + 3)
				count = page + 3

	response.update({'counter':counter})
	response.update({'count':count})
	response.update({'pages':pages})
	response.update({'last':last})

	response.update({'questions':questions[(page*3):(page*3)+3]})
	return render_to_response('tutor_home.html',response)   
