from django.conf.urls import patterns, include, url

import pscexams.forum.views

urlpatterns = patterns('',
	url(r'^ask/$', pscexams.forum.views.ask_question, name='ask-question'),
	url(r'^view/(?P<pk>\w+)/(?P<slug>[-\w]+)/$', pscexams.forum.views.view_question, name='view-question'),
	url(r'^submit/answer/$', pscexams.forum.views.submit_answer, name='submit-answer'),
	url(r'^submit/comment/$', pscexams.forum.views.submit_question_comment, name='submit-question-comment'),
	url(r'^submit/answer/comment/$', pscexams.forum.views.submit_answer_comment, name='submit-answer-comment'),
	url(r'^vote/$', pscexams.forum.views.question_vote, name='question-vote'),
	url(r'^answer/vote/$', pscexams.forum.views.answer_vote, name='answer-vote'),
	url(r'^unanswered/$', pscexams.forum.views.question_unanswered, name='question-unanswered'),
	url(r'^answered/$', pscexams.forum.views.question_answered, name='question-answered'),
	url(r'^resolved/$', pscexams.forum.views.question_resolved, name='question-resolved'),
	url(r'^closed/$', pscexams.forum.views.question_closed, name='question-closed'),
	url(r'^tag/(?P<tag>[-\w]+)/$', pscexams.forum.views.tag_questions, name='tag-questions'),
	url(r'^search/(?P<search>[-\w]+)/$', pscexams.forum.views.search_questions, name='search-questions'),
	url(r'^approve/answer/$', pscexams.forum.views.approve_answer, name='approve-answer'),
	url(r'^close/$', pscexams.forum.views.question_close, name='question-close'),
	url(r'^reopen/$', pscexams.forum.views.question_reopen, name='question-reopen'),
)
