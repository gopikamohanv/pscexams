from django.db import models
from django.contrib.auth.models import *


class State(models.Model):
	state = models.CharField(max_length=30)

	def __unicode__(self):
		return self.state


class Exam(models.Model):
	state = models.ForeignKey(State)
	exam = models.CharField(max_length=30)
	image = models.CharField(max_length=255, null=True, blank=True)

	def __unicode__(self):
		return self.state.state + '->' + str(self.exam)


class Subject(models.Model):
	state = models.ForeignKey(State)
	exam = models.ForeignKey(Exam)
	subject = models.CharField(max_length=30)

	def __unicode__(self):
		return self.state.state + '->' + self.exam.exam + '->' + str(self.subject)


class Topic(models.Model):
	state = models.ForeignKey(State)
	exam = models.ForeignKey(Exam)
	subject = models.ForeignKey(Subject)
	topic = models.CharField(max_length=30)

	def __unicode__(self):
		return self.state.state + '->' + self.exam.exam + '->' + self.subject.subject + '->' + str(self.topic)


class Question(models.Model):
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    answer = models.CharField(max_length=2)
    explanation = models.TextField(null=True)
    tutor = models.ForeignKey(User, related_name='question_tutor')
    publisher = models.ForeignKey(User, related_name='question_publisher', null=True, blank=True)
    is_published = models.BooleanField()
    topic = models.ForeignKey(Topic)
    mode = models.CharField(max_length=2)
    created_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_in_use = models.BooleanField()     # When deleting, set this to false, not delete the object
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question
