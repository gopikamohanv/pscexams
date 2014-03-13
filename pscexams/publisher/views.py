from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from pscexams.user_type import UserType
from pscexams.exam_type import ExamType
from pscexams.admin.models import *
from pscexams.student.models import UserProfile

import datetime
import math

#PAGE_LIMIT=20

#def pagination(page,count,limit):
    #response = {}
    
    #limit = limit
    # to show the page notion 
    #counter = page * limit
    #pages = int(math.ceil(float(count)/limit)) 
    
    #if page > pages:
        #raise Http404()
    
    #last = pages - 1
    #if pages <= 5:
        #pages = range(0,pages)
        #count_page = 0
    #else:   
        #if page <= 2: 
            #pages = range(0,5)
            #count_page = 4
        #else:
            #if page == last or page == last - 1 :
                #pages = range(page - 2 , pages)
                #count_page = last + 1
            #else:
                #pages = range(page - 2, page + 3)
                #count_page = page + 3  
    
    #response.update({'pages':pages})          
    #response.update({'count':count_page})
    #response.update({'last':last})
    #response.update({'counter':counter})
    #return response


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
	                modelexam_questions = ModelExamQuestion()
	                modelexam_questions.modelexam = test_obj
	                modelexam_questions.question = qn_obj
	                try:
	                    modelexam_questions.save()
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
		questions = Question.objects.filter(sub_topic=sub_topic, question_type='2')
		response.update({'questions':questions})
		count = questions.count()
		response.update({'count':count})
	except:
		response.update({'no_questions':True})
	return render_to_response('ajax_add_question.html', response)


# Ajax for tutor question search
# /subtopic/ajax/questions/
def subtopic_ajax_publisher_question(request):
	response = {}
	if 'sub_topic' in request.GET and request.GET['sub_topic']:
		sub_topic = request.GET['sub_topic']

	#if 'page' in request.GET and request.GET['page']:
		#page = request.GET['page']

	try:
		questions = Question.objects.filter(sub_topic=sub_topic)
		response.update({'questions':questions})
	except:
		response.update({'no_questions':True})

	#page = int(page)
	#limit = PAGE_LIMIT
	#response.update({'current_page':page})
	#pages = pagination(page, questions.count(), limit)
	#response.update({'pages':pages})
	#response.update({'questions':questions[(page*limit):(page*limit)+limit]})
	return render_to_response('ajax_publisher_questions.html', response)


# Browse questions of assigned subjects
# /publisher/ajax/browse/questions/
#def publisher_ajax_browse_questions(request):
    #response = {}
    #response.update(csrf(request))

    #return HttpResponse('gfgf')

    #if not request.user.is_authenticated():
        #raise Http404

    #response.update({'user':request.user})

   #try:
        #user_profile = UserProfile.objects.get(user=request.user)
    #except:
        #raise Http500
    #if user_profile.user_type != UserType.types['Publisher']:
        #raise Http404()

    #form_error = False
    #if 'sub_topic' in request.GET and request.GET['sub_topic']:
        #sub_topic = request.GET['sub_topic']
    #else:
        #raise Http404
    #if 'next_rows' in request.GET and request.GET['next_rows']:
        #next_rows = request.GET['next_rows']
        #next_rows = int(next_rows)
    #else:
        #next_rows = 0
    #questions = Question.objects.filter(sub_topic=sub_topic, is_in_use=True)
   
    #if next_rows == 0:
        #questions = questions[:20]
    #else:
        #questions = questions[next_rows:next_rows + 20]
    #response.update({'questions':questions})
    #if not questions:
        #return HttpResponse('False')
    #response.update({'current_counter':next_rows})
    #if next_rows == 0:
        #return render_to_response('ajax_publisher_questions.html', response)
    #else:
        #return render_to_response('ajax_questions.html', response)


# AJAXly publish a question
# /publisher/question/ajax/publish/
def publisher_questions_ajax_publish(request):
	response = {}
	response.update(csrf(request))
	
	if not request.user.is_authenticated:
		raise Http404

	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		raise Http500

	
	if user_profile.user_type != UserType.types['Publisher']:
		raise Http404()

	if 'qid' in request.POST and request.POST['qid']:
		question_id = request.POST['qid']
	else:
		return HttpResponse('Null')
	try:
		question = Question.objects.get(id=question_id)
	except:
		return HttpResponse('Null')

	question.is_published = True
	question.publisher = request.user
	question.published_date = datetime.datetime.today()
	try:
		question.save()
	except:
		return HttpResponse('Null')

	return HttpResponse('Success')
    
# AJAXly unpublish a question
# /publisher/question/ajax/unpublish/
def publisher_questions_ajax_unpublish(request):

    response = {}
    response.update(csrf(request))
    if not request.user.is_authenticated:
        raise Http404
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http500
    if user_profile.user_type != UserType.types['Publisher']:
        raise Http404()    
    
    if 'qid' in request.POST and request.POST['qid']:
        question_id = request.POST['qid']
    else:
        return HttpResponse('Null')

    try:
        question = Question.objects.get(id=question_id)
    except:
        return HttpResponse('Null')


    # Un-Publish the Question
    question.is_published = False
    try:
        question.save()
    except:
        return HttpResponse('Null')
 
    return HttpResponse('Success')


# /publisher/questions/edit/
def publisher_questions_edit(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http500

    if user_profile.user_type != UserType.types['Publisher']:
        return HttpResponseRedirect(DefaultUrl.login_url)

    response = {}
    response.update(csrf(request))

    states = State.objects.all()
    response.update({'states':states})

    if request.method == 'GET':
        if 'id' in request.GET and request.GET['id']:
            question_id = request.GET['id']
        else:
        	response.update({'error':True})
        	return render_to_response('publisher_home.html', response)

        try:
            question_obj = Question.objects.get(id=question_id)
        except:
        	raise Http404()
       
        response.update({'question_obj':question_obj})
        exams = Exam.objects.filter(state=question_obj.sub_topic.state)
    	subjects = Subject.objects.filter(exam=question_obj.sub_topic.exam)
    	topics = Topic.objects.filter(subject=question_obj.sub_topic.subject)
    	sub_topics = SubTopic.objects.filter(topic=question_obj.sub_topic.topic)
    	response.update({'exams':exams})
    	response.update({'subjects':subjects})
    	response.update({'topics':topics})
    	response.update({'sub_topics':sub_topics})
    	return render_to_response('publisher_question_edit.html', response)

    
    if request.method == 'POST':
	    if 'question_id' in request.POST and request.POST['question_id']:
	        question_id = request.POST['question_id']
	    else:
	        response.update({'error':True})
    		return render_to_response('publisher_home.html', response)
	    try:
	        question_obj = Question.objects.get(id=question_id)
	    except:
	        raise Http404()

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

	    if 'sub_topic' in request.POST and request.POST['sub_topic']:
	       sub_topic  = request.POST['sub_topic']
	       if sub_topic == '0':
	           form_error = True
	    else:
	        form_error = True

	    if 'question_type' in request.POST and request.POST['question_type']:
	        question_type = request.POST['question_type']
	        if question_type == '0':
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
	        return render_to_response('publisher_question_edit.html', response)

	    

	    data_error = False
	    try:
	        sub_topic_obj = SubTopic.objects.get(id=sub_topic)
	    except:
	        data_error = True
	    if data_error:
	        response.update({'form_error':True})
	        response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
	        return render_to_response('publisher_question_edit.html', response)

	    
	    question_obj.question = question
	    question_obj.option1 = option1
	    question_obj.option2 = option2
	    question_obj.option3 = option3
	    question_obj.option4 = option4
	    question_obj.answer = answer_in_option
	    question_obj.explanation = explanation
	    question_obj.is_published = False
	    question_obj.sub_topic = sub_topic_obj
	    question_obj.question_type = question_type 
	    question_obj.is_in_use = True

	    try:
	    	question_obj.save()
	    	response.update({'question_saved':True})
	    except:
	    	response.update({'form_error':True})
	    	response.update({'error_text':'Error occured while saving your question. If this problem repeats, please contact the Smart World Technical team'})
	    	return render_to_response('publisher_question_edit.html', response)

	    response.update({'question_obj':question_obj})
	    exams = Exam.objects.filter(state=question_obj.sub_topic.state)
	    subjects = Subject.objects.filter(exam=question_obj.sub_topic.exam)
	    topics = Topic.objects.filter(subject=question_obj.sub_topic.subject)
	    sub_topics = SubTopic.objects.filter(topic=question_obj.sub_topic.topic)
	    response.update({'exams':exams})
	    response.update({'subjects':subjects})
	    response.update({'topics':topics})
	    response.update({'sub_topics':sub_topics})
	    return render_to_response('publisher_question_edit.html', response)