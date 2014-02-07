from django.db import models
from django.contrib.auth.models import *


class State(models.Model):
	state = models.CharField(max_length=255)

	def __unicode__(self):
		return self.state


class Exam(models.Model):
	state = models.ForeignKey(State)
	exam = models.CharField(max_length=255)
	image = models.CharField(max_length=255, null=True, blank=True)

	#def __unicode__(self):
	#	return self.state.state + '->' + str(self.exam)


class Subject(models.Model):
	state = models.ForeignKey(State)
	exam = models.ForeignKey(Exam)
	subject = models.CharField(max_length=255)

	#def __unicode__(self):
	#	return self.state.state + '->' + self.exam.exam + '->' + str(self.subject)

class SubjectDescription(models.Model):
	subject = models.OneToOneField(Subject)
	image = models.CharField(max_length=255, null=True, blank=True)
	description = models.TextField()

	def __unicode__(self):
		return str(self.subject)

class Topic(models.Model):
	state = models.ForeignKey(State)
	exam = models.ForeignKey(Exam)
	subject = models.ForeignKey(Subject)
	topic = models.CharField(max_length=255)

	#def __unicode__(self):
	#	return self.state.state + '->' + self.exam.exam + '->' + self.subject.subject + '->' + str(self.topic)

class SubTopic(models.Model):
	state = models.ForeignKey(State)
	exam = models.ForeignKey(Exam)
	subject = models.ForeignKey(Subject)
	topic = models.ForeignKey(Topic)
	sub_topic = models.CharField(max_length=255)
	descripition = models.TextField()


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
    sub_topic = models.ForeignKey(SubTopic)
    question_type = models.CharField(max_length=2)
    created_date = models.DateTimeField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_in_use = models.BooleanField()     # When deleting, set this to false, not delete the object
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.question


class ModelExam(models.Model):
	title = models.CharField(max_length=250)
	exam = models.ForeignKey(Exam)
	max_question = models.CharField(max_length=5)
	max_time = models.CharField(max_length=5, null=True, blank=True)
	is_published = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

class ModelExamQuestion(models.Model):
	modelexam = models.ForeignKey(ModelExam)
	question = models.ForeignKey(Question)


class ExamDescription(models.Model):
	exam = models.ForeignKey(Exam)
	description = models.CharField(max_length=255)

	def __unicode__(self):
		return self.exam.exam
