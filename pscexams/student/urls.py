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
		(r'^onewords/(?P<pk>\w+)/$', pscexams.student.views.student_onewords),
		(r'^tips/topics/(?P<pk>\w+)/$', pscexams.student.views.student_tips_topics),
		(r'^tips/view/(?P<pk>\w+)/$', pscexams.student.views.student_tips_view),
		(r'^question/new/(?P<pk>\w+)/$', pscexams.student.views.student_question_new),
		(r'^trick/new/(?P<pk>\w+)/$', pscexams.student.views.student_trick_new),
		(r'^performance/(?P<pk>\w+)/$', pscexams.student.views.student_performance),
		(r'^myprofile/$', pscexams.student.views.student_profile),
		(r'^password/reset/$', pscexams.student.views.student_password_reset),
		(r'^previousyearexam/download/(?P<pk>\w+)/$', pscexams.student.views.student_previous_year_exam),
)