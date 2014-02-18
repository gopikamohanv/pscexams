from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

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

	if user_type == '0':
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
			response.update({'question_saved':True})
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
			response.update({'question_saved':True})
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
			response.update({'question_saved':True})
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
			response.update({'question_saved':True})
		except:
			response.update({'save_error':True})

		return render_to_response('add_sub_topic.html', response)
		