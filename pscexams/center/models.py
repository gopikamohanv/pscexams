from django.db import models
from django.contrib.auth.models import *


class Center(models.Model):
	student = models.ForeignKey(User, related_name='student')
	center = models.ForeignKey(User, related_name='center')

	def __unicode__(self):
		return self.center