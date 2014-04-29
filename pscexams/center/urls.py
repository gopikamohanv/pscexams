from django.conf.urls import patterns, include, url
import pscexams.center.views

urlpatterns = patterns('',

		(r'^dashboard/$', pscexams.center.views.center_dashboard),
		(r'^add/user/$', pscexams.center.views.center_add_users),


)