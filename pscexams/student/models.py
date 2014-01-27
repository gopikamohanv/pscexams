from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import User
from pscexams.user_type import UserType
from pscexams.admin.models import *
# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	user_type= models.CharField(max_length=10)
	state =  models.ForeignKey(State, null=True, blank=True)
	mobile_no = models.CharField(max_length=10, null=True, blank=True)
	address = models.CharField(max_length=30, null=True, blank=True)
	def __unicode__(self):
		return self.user_type
