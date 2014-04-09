from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

import datetime

# Question Model 
class Question(models.Model):
		title = models.TextField()
		description = models.TextField()
		created_by = models.ForeignKey(User)
		created_on = models.DateTimeField(null=True, blank=True)
		updated_on = models.DateTimeField(auto_now=True)
		accepted = models.BooleanField(default=False)
		slug = models.SlugField(db_index=True)
		approved = models.BooleanField(default=False)
		closed = models.BooleanField(default=False)

		def __unicode__(self):
			return self.created_by.username

		class Meta:
			ordering = ['-id']

		def save(self, *args, **kwargs):
				if not self.id:
						# This is a first time creation
						self.created_on = datetime.datetime.now()
				super(Question, self).save(*args, **kwargs)

		def getvotescount(self):
			upvotes = QuestionVotes.objects.filter(question=self, up_vote=True).count()
			downvotes = QuestionVotes.objects.filter(question=self, down_vote=True).count() 	
			return upvotes - downvotes

		def getanswerscount(self):
			return Answer.objects.filter(question=self, approved=True).count()


# Answer Model        
class Answer(models.Model):
		question = models.ForeignKey(Question)
		answer = models.TextField()
		answered_by = models.ForeignKey(User)
		answered_on = models.DateTimeField(null=True, blank=True)
		updated_on = models.DateTimeField(auto_now=True)
		accepted = models.BooleanField(default=False)
		approved = models.BooleanField(default=False)

		def save(self, *args, **kwargs):
				if not self.id:
						# This is a first time creation
						self.answered_on = datetime.datetime.now()
				super(Answer, self).save(*args, **kwargs)

		def getvotescount(self):
			upvotes = AnswerVotes.objects.filter(answer=self, up_vote=True).count()
			downvotes = AnswerVotes.objects.filter(answer=self, down_vote=True).count()
			return upvotes - downvotes

		def __unicode__(self):
			return self.answered_by.username

# Votes for question
class QuestionVotes(models.Model):
		question = models.ForeignKey(Question)
		voted_by = models.ForeignKey(User)
		up_vote = models.BooleanField(default=False)
		down_vote = models.BooleanField(default=False)
		voted_on = models.DateTimeField(auto_now=True, null=True, blank=True)

class QuestionView(models.Model):
		question = models.ForeignKey(Question)

# Votes for answer
class AnswerVotes(models.Model):
		answer = models.ForeignKey(Answer)
		voted_by = models.ForeignKey(User)
		up_vote = models.BooleanField(default=False)
		down_vote = models.BooleanField(default=False)
		voted_on = models.DateTimeField(auto_now=True, null=True, blank=True)

# Tag Model
class Tag(models.Model):
		tag = models.CharField(max_length=255)
		slug = models.SlugField(db_index=True)

# Tags in Question
class QuestionTag(models.Model):
		question = models.ForeignKey(Question)
		tag = models.ForeignKey(Tag)

# Comment Model for question and answer
class Comment(models.Model):
		question = models.ForeignKey(Question, null=True, blank=True)
		answer = models.ForeignKey(Answer, null=True, blank=True)
		comment = models.TextField()
		commented_by = models.ForeignKey(User)
		commented_on = models.DateTimeField(null=True, blank=True)
		updated_on = models.DateTimeField(auto_now=True)
		approved = models.BooleanField(default=False)

		def __unicode__(self):
			return self.commented_by.username

		def save(self, *args, **kwargs):
				if not self.id:
						# This is a first time creation
						self.commented_on = datetime.datetime.now()
				super(Comment, self).save(*args, **kwargs)

# Comment votes
class CommentVotes(models.Model):
		comment = models.ForeignKey(Comment)
		voted_by = models.ForeignKey(User)

class Ad(models.Model):
	ad_url = models.CharField(max_length=255)


def getPoints(self):
	points = 0

	# Approved Question
	points = points + self.getApprovedQuestions() * 5

	# Approved Answers
	points = points + self.getApprovedAnswers() * 5

	# Accepted Answers
	points = points + self.getAcceptedAnswers() * 10

	# Total Votes
	points = points + self.getVotes()

	return points

def getApprovedQuestions(self):
	questions = Question.objects.filter(created_by=self, approved=True)
	return questions.count()

def getQuestionsPoints(self):
	questions = Question.objects.filter(created_by=self, approved=True)
	return questions.count() * 5

def getApprovedAnswers(self):
	answers = Answer.objects.filter(answered_by=self, approved=True)
	return answers.count()

def getAnswersPoints(self):
	answers = Answer.objects.filter(answered_by=self, approved=True)
	return answers.count() * 5

def getAcceptedAnswers(self):
	answers = Answer.objects.filter(answered_by=self, accepted=True)
	return answers.count()

def getAcceptedAnswersPoints(self):
	answers = Answer.objects.filter(answered_by=self, accepted=True)
	return answers.count() * 10

def getVotes(self):
	votes = 0
	# Question Votes
	questions = Question.objects.filter(created_by=self, approved=True)
	for q in questions:
		votes = votes + q.getvotescount()

	# Answer Votes
	answers = Answer.objects.filter(answered_by=self, approved=True)
	for a in answers:
		votes = votes  + a.getvotescount()

	return votes

auth.models.User.add_to_class('getPoints', getPoints)
auth.models.User.add_to_class('getQuestionsPoints', getQuestionsPoints)
auth.models.User.add_to_class('getAnswersPoints', getAnswersPoints)
auth.models.User.add_to_class('getAcceptedAnswersPoints', getAcceptedAnswersPoints)
auth.models.User.add_to_class('getApprovedQuestions', getApprovedQuestions)
auth.models.User.add_to_class('getApprovedAnswers', getApprovedAnswers)
auth.models.User.add_to_class('getAcceptedAnswers', getAcceptedAnswers)
auth.models.User.add_to_class('getVotes', getVotes)


