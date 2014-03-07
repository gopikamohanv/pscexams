from django.conf.urls import patterns, include, url
import pscexams.modelexam.views

urlpatterns = patterns('',

		(r'^modelexam/(?P<pk>\w+)/$', pscexams.modelexam.views.student_modelexam),
		(r'^modelexam/start/(?P<pk>\w+)/$', pscexams.modelexam.views.student_modelexam_start),
		(r'^modelexam/(?P<pk>\w+)/submit/$', pscexams.modelexam.views.student_modelexam_submit),
		(r'^modelexam/download/(?P<pk>\w+)/$', pscexams.modelexam.views.student_modelexam_download),
)