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


# MOCK TEST
class MockTest(models.Model):
    user = models.ForeignKey(UserProfile)
    test_date = models.DateTimeField(auto_now=True)
    correct_answers = models.CharField(max_length=4)
    score = models.IntegerField(null=True, blank=True)
    time_taken = models.CharField(max_length=4, null=True, blank=True)
    
class MockTestData(models.Model):
    mock_test = models.ForeignKey(MockTest)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=2)
    answered = models.BooleanField()
    
class MockTestType(models.Model):
    mock_test_type = models.CharField(max_length=4)
    mock_test = models.ForeignKey(MockTest)
