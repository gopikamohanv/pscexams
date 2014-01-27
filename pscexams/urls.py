from django.conf.urls import patterns, url, include
from pscexams.views import *
from tutor.views import *
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


	(r'^$',index),
	(r'^login/$',login_view),
	(r'^home/$',home),
	(r'^tutor/questions/add/$',tutor_questions_add),
    (r'^state/ajax/exam/$',state_ajax_exam),
    (r'^exam/ajax/subject/$',exam_ajax_subject),
    (r'^subject/ajax/topic/$',subject_ajax_topic),
    (r'^tutor/questions/edit/$', tutor_questions_edit),
    (r'^logout/$', logout_view),
    (r'^register/$', register),
)