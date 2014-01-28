from django.conf.urls import patterns, include, url
import pscexams.student.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.student.views.student_dashboard),
		(r'^exam/(?P<pk>\w+)/$', pscexams.student.views.student_exam),
		(r'^exam/(?P<pk>\w+)/submit/$', pscexams.student.views.student_exam_submit),
)