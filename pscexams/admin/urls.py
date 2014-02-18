from django.conf.urls import patterns, include, url
import pscexams.admin.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.admin.views.admin_dashboard),
		#(r'^users/$', pscexams.admin.views.user_list),
		(r'^users/ajax/browse/$', pscexams.admin.views.siteadmin_user_ajax_browse),
		(r'^ajax/users/search/$', pscexams.admin.views.siteadmin_ajax_users_search_username),
		(r'^add/exam/$', pscexams.admin.views.admin_add_exam),
		(r'^add/subject/$', pscexams.admin.views.admin_add_subject),
		(r'^add/topic/$', pscexams.admin.views.admin_add_topic),
		(r'^add/subtopic/$', pscexams.admin.views.admin_add_sub_topic),
		(r'^upload/modelexam/question/$', pscexams.admin.views.admin_upload_modelexamquestion),
		(r'^upload/previousyear/question/$', pscexams.admin.views.admin_upload_previousyearquestion),
)