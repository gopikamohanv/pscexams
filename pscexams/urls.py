from django.conf.urls import patterns, url, include
from pscexams.views import *
from pscexams.tutor.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
import forum.views

urlpatterns = patterns('',
    # Example:
    # (r'^outsource/', include('outsource.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),


    # URL for index pages
    (r'^$',index),
    (r'^login/$',login_view),
    (r'^home/$',home),
    (r'^tutor/questions/add/$',tutor_questions_add),
    (r'^state/ajax/exam/$',state_ajax_exam),
    (r'^exam/ajax/subject/$',exam_ajax_subject),
    (r'^subject/ajax/topic/$',subject_ajax_topic),
    (r'^subtopic/ajax/oneword/$',subtopic_ajax_oneword),
    (r'^tutor/questions/edit/$', tutor_questions_edit),
    (r'^logout/$', logout_view),
    (r'^register/$', register),
    (r'^registration/$', registration_add),
    (r'^about/$',about),
    (r'^smartindia/$',smartindia),
    (r'^keralapsc/$',keralapsc),
    (r'^topic/ajax/subtopic/$',topic_ajax_subtopic),
    (r'^subtopic/ajax/question/$',subtopic_ajax_question),
    (r'^tutor/myaccount/$',tutor_myaccount),
    (r'^about/previous/year/question/$',about_previous_year_question),
    (r'^about/modelexams/$',about_model_exams),
    (r'^about/tipsandtricks/$',about_tipsandtricks),
    (r'^about/readandlearn/$',about_readandlearn),
    (r'^about/new/$',about_new),
    (r'^about/examcategory/$',about_examcategory),
    (r'^about/subject/topics/$',about_subject_topics),
    (r'^about/topic/subtopic/$',about_topic_subtopic),
    (r'^contact/$',contact),
    (r'^list/modelexams/$',list_modelexams_free),
    (r'^list/tipsandtricks/(?P<pk>\w+)/$',list_tipsandtricks),
    (r'^practice/$',free_practice),
    (r'^practice/test/$',free_practice_test),
    (r'^practice/start/(?P<pk>\w+)/$',free_practice_start),
    (r'^ajax/practice/free/$',ajax_practice_free),
    (r'^free/modelexam/(?P<pk>\w+)/$',free_modelexam),
    (r'^free/modelexam/(?P<pk>\w+)/$',free_modelexam),
    (r'^free/modelexam/download/(?P<pk>\w+)/$',free_modelexam_download),
    (r'^free/previous/exam/(?P<pk>\w+)/$',free_previous_exam),
    (r'^free/tricks/(?P<pk>\w+)/$',free_tricks),
    (r'^free/tricks/detail/(?P<pk>\w+)/$',free_tricks_detail),
    (r'^free/learn/(?P<pk>\w+)/$',free_learn),
    (r'^subtopic/content/$',sub_topic_content),
    (r'^language/ajax/topic/$',language_ajax_topic),


    # Student Urls
    url(r'^student/', include('pscexams.student.urls')),
    url(r'^publisher/', include('pscexams.publisher.urls')),
    url(r'^siteadmin/', include('pscexams.admin.urls')),
    url(r'^tutor/', include('pscexams.tutor.urls')),
    url(r'^student/', include('pscexams.modelexam.urls')),

    #forum Urls
    url(r'^user/$', forum.views.user, name='user'),
    url(r'^user/delete/question/$', forum.views.user_delete_question, name='user-delete-question'),
    url(r'^user/delete/answer/$', forum.views.user_delete_answer, name='user-delete-answer'),
    url(r'^user/delete/comment/$', forum.views.user_delete_comment, name='user-delete-comment'),
    url(r'^user/edit/question/(?P<pk>\w+)/$', forum.views.user_edit_question, name='user-edit-question'),
    url(r'^user/edit/answer/$', forum.views.user_edit_answer, name='user-edit-answer'),
    url(r'^user/edit/comment/$', forum.views.user_edit_comment, name='user-edit-comment'),
    url(r'^users/$', forum.views.users, name='users'),
    url(r'^userdetails/(?P<pk>\w+)/$', forum.views.userdetails, name="user-details"),
    url(r'^getAnswer/$', forum.views.get_answer, name='get-answer'),
    url(r'^loadmore/users/$', forum.views.loadmore_users, name='loadmore-users'),
    url(r'^forum/$', forum.views.index, name='forum'),
    url(r'^getTags/$', forum.views.get_tags, name='get-tags'),
    url(r'^question/', include('pscexams.forum.urls', namespace='question')),


)