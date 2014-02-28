from django.conf.urls import patterns, include, url
import pscexams.tutor.views

urlpatterns = patterns('',

		(r'^mcqs/$', pscexams.tutor.views.tutor_mcqs),
		(r'^oneword/$', pscexams.tutor.views.tutor_oneword),
		(r'^oneword/list/$', pscexams.tutor.views.tutor_oneword_list),
		(r'^oneword/edit/$', pscexams.tutor.views.tutor_oneword_edit),
		(r'^add/tipsandtricks/$', pscexams.tutor.views.tutor_add_tips_and_tricks),
		
)