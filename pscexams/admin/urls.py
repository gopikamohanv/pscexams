from django.conf.urls import patterns, include, url
import pscexams.admin.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.admin.views.admin_dashboard),
		(r'^users/workdetails/$', pscexams.admin.views.user_workdetails),
		(r'^users/ajax/browse/$', pscexams.admin.views.siteadmin_user_ajax_browse),
		(r'^ajax/users/search/$', pscexams.admin.views.siteadmin_ajax_users_search_username),
		(r'^add/exam/$', pscexams.admin.views.admin_add_exam),
		(r'^add/subject/$', pscexams.admin.views.admin_add_subject),
		(r'^add/topic/$', pscexams.admin.views.admin_add_topic),
		(r'^add/subtopic/$', pscexams.admin.views.admin_add_sub_topic),
		(r'^upload/modelexam/question/$', pscexams.admin.views.admin_upload_modelexamquestion),
		(r'^upload/previousyear/question/$', pscexams.admin.views.admin_upload_previousyearquestion),
		(r'^forum/questions/$', pscexams.admin.views.questions),
		(r'^forum/answers/$', pscexams.admin.views.answers),
		(r'^forum/comments/$', pscexams.admin.views.comments),
		(r'^approve/question/$', pscexams.admin.views.approve_question),
		(r'^delete/question/$', pscexams.admin.views.delete_question),
		(r'^approve/answer/$', pscexams.admin.views.approve_answer),
		(r'^delete/answer/$', pscexams.admin.views.delete_answer),
		(r'^approve/comment/$', pscexams.admin.views.approve_comment),
		(r'^delete/comment/$', pscexams.admin.views.delete_comment),
		(r'^send_message/$', pscexams.admin.views.send_message),
)