from django.conf.urls import patterns, include, url
import pscexams.publisher.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.publisher.views.publisher_dashboard),
		(r'^create/modelexam/$', pscexams.publisher.views.publisher_create_modelexam),
		(r'^select/modelexam/questions/$', pscexams.publisher.views.publisher_select_modelexam_questions),
		(r'^modelexam/ajax/question/$', pscexams.publisher.views.modelexam_ajax_question),
		(r'^add/modelexam/questions/$', pscexams.publisher.views.publisher_add_modelexam_questions),
		(r'^subtopic/ajax/add/question/$', pscexams.publisher.views.subtopic_ajax_add_question),
		(r'^subtopic/ajax/questions/$', pscexams.publisher.views.subtopic_ajax_publisher_question),
		#(r'^ajax/browse/questions/$', pscexams.publisher.views.publisher_ajax_browse_questions),
		(r'^question/ajax/publish/$', pscexams.publisher.views.publisher_questions_ajax_publish),
		(r'^question/ajax/unpublish/$', pscexams.publisher.views.publisher_questions_ajax_unpublish),
		(r'^questions/edit/$', pscexams.publisher.views.publisher_questions_edit),
		
)