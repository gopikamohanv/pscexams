from django.db import models
from django.contrib.auth.models import *
from django.contrib.auth.models import User


class CurrentAffair_Language(models.Model):
	language = models.CharField(max_length=15)

	def __unicode__(self):
		return self.language

class CurrentAffairs_topic(models.Model):
	language = models.ForeignKey(CurrentAffair_Language)
	topic = models.CharField(max_length=20)

class CurrentAffairs_Question(models.Model):
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.CharField(max_length=2, null=True)
    explanation = models.TextField(null=True)
    tutor = models.ForeignKey(User, related_name='currentaffair_question_tutor')
    publisher = models.ForeignKey(User, related_name='currentaffair_question_publisher', null=True, blank=True)
    is_published = models.BooleanField()
    topic = models.ForeignKey(CurrentAffairs_topic)
    created_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_in_use = models.BooleanField()     # When deleting, set this to false, not delete the object
    last_modified = models.DateTimeField(auto_now=True)


class CurrentAffairs_OnewordQuestion(models.Model):
    question = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(null=True)
    topic = models.ForeignKey(CurrentAffairs_topic)
    tutor = models.ForeignKey(User, related_name='currentaffair_oneword_tutor')
    publisher = models.ForeignKey(User, related_name='currentaffair_oneword_publisher', null=True, blank=True)
    is_published = models.BooleanField()
    created_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_in_use = models.BooleanField()     # When deleting, set this to false, not delete the object
    last_modified = models.DateTimeField(auto_now=True)