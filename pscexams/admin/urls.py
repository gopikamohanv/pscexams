from django.conf.urls import patterns, include, url
import pscexams.admin.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.admin.views.admin_dashboard),
		(r'^add/exam/$', pscexams.admin.views.admin_add_exam),
		(r'^add/subject/$', pscexams.admin.views.admin_add_subject),
		(r'^add/topic/$', pscexams.admin.views.admin_add_topic),
		(r'^add/subtopic/$', pscexams.admin.views.admin_add_sub_topic),
)