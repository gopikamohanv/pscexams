from django.conf.urls import patterns, url, include
from pscexams.views import *
from pscexams.tutor.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^outsource/', include('outsource.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),


    # URL for index pages
    (r'^$',index),
    (r'^about/$',about),
    (r'^smartindia/$',smartindia),
    (r'^keralapsc/$',keralapsc),

   
    # URL for login according to usertype
    (r'^login/$',user_login),
    (r'^home/$',home),


    # URL for registration
    (r'^registration/$', registration_add),
    

    # URL for tutor pages
    (r'^tutor/questions/add/$',tutor_questions_add),
    (r'^tutor/questions/edit/$', tutor_questions_edit),
    (r'^questions/browse/$', tutor_questions_edit),
    

    # URL for ajax 
    (r'^state/ajax/exam/$',state_ajax_exam),
    (r'^exam/ajax/subject/$',exam_ajax_subject),
    (r'^subject/ajax/topic/$',subject_ajax_topic),


    # URL for logout
    (r'^logout/$', user_logout),
)