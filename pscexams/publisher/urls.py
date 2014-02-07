from django.conf.urls import patterns, include, url
import pscexams.publisher.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.publisher.views.publisher_dashboard),
		(r'^create/modelexam/$', pscexams.publisher.views.publisher_create_modelexam),
		(r'^select/modelexam/questions/$', pscexams.publisher.views.publisher_select_modelexam_questions),
		(r'^modelexam/ajax/question/$', pscexams.publisher.views.modelexam_ajax_question),
		(r'^add/modelexam/questions/$', pscexams.publisher.views.publisher_add_modelexam_questions),
		(r'^subtopic/ajax/add/question/$', pscexams.publisher.views.subtopic_ajax_add_question),
		#(r'^exam/(?P<pk>\w+)/submit/$', pscexams.student.views.student_exam_submit),
		#(r'^answersheets/list/$', pscexams.student.views.student_answersheets_list),
		#(r'^answersheet/(?P<pk>\w+)/$', pscexams.student.views.student_answersheet),
)