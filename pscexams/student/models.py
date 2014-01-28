from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import User
from pscexams.user_type import UserType
from pscexams.admin.models import *
# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	user_type= models.CharField(max_length=10)
	state =  models.ForeignKey(State)
	name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	mobile_no = models.CharField(max_length=10)
	def __unicode__(self):
		return self.user_type
