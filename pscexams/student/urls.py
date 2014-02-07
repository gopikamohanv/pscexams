from django.conf.urls import patterns, include, url
import pscexams.student.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.student.views.student_dashboard),
		(r'^exam/(?P<pk>\w+)/$', pscexams.student.views.student_exam),
		(r'^exam/subject/(?P<pk>\w+)/$', pscexams.student.views.student_exam_subject),
		(r'^exam/topic/tests/(?P<pk>\w+)/$', pscexams.student.views.student_exam_topic_tests),
		(r'^exam/topic/(?P<pk>\w+)/(?P<test>\w+)/$', pscexams.student.views.student_exam_topic),
		(r'^exam/(?P<pk>\w+)/submit/$', pscexams.student.views.student_exam_submit),
		(r'^answersheets/list/$', pscexams.student.views.student_answersheets_list),
		(r'^answersheet/(?P<pk>\w+)/$', pscexams.student.views.student_answersheet),
)