from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from pscexams.user_type import UserType
from pscexams.admin.models import Exam, Question
from pscexams.student.models import UserProfile

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
	exam = get_object_or_404(Exam, pk=pk)
	response.update({'user':UserProfile.objects.get(user=request.user)})
	questions = Question.objects.filter(topic__exam=exam)
	response.update({'questions':questions})
	return render_to_response('student_exam.html', response)

@login_required
@user_passes_test(student_check)
def student_exam_submit(request):
	response = {}
	
	


