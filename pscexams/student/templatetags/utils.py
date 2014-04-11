from django import template
from pscexams.student.models import ExamTest
import time

register = template.Library()


@register.filter
def getExamStatus(user, subtopic):
	try:
		test_num = ExamTest.objects.get(user=user, exam_topic=subtopic)
	except:
		return 0
	else:
		return test_num.test_num + 1

@register.filter
def getTimeInSec(user):
	return int(time.mktime(user.date_joined.timetuple()) * 1000)