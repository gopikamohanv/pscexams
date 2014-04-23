from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template.defaultfilters import slugify
from django.contrib import auth
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from pscexams.forum.models import Question, QuestionView, Tag, QuestionTag, Answer, Comment, QuestionVotes, AnswerVotes, Ad

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.mail import mail_admins
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import random
import string
import datetime
import json

def pagination(questions, page=1):
	paginator = Paginator(questions, 20)

	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		questions = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		questions = paginator.page(paginator.num_pages)
	return questions

def check_auth(request):
		if not request.user.is_authenticated():
				return True
		else:
				return False

def index(request):
		response = {}
		response.update({'not_authenticated':check_auth(request)})
		response.update({'user':request.user})
		response.update({'status':'All Questions'})
		response.update({'next':request.get_full_path()})

		sort = False
		if 'sort_by' in request.GET and request.GET['sort_by']:
			sort_by = request.GET['sort_by']
			sort = True

		if sort:
			if sort_by == 'latest':
				questions = Question.objects.filter(approved=True).order_by('-pk')
				response.update({'status':'Latest Questions'})
				response.update({'latest':True})
			elif sort_by == 'most_voted':
				questions  = Question.objects.filter(approved=True).exclude(questionvotes=None).annotate(upvotes=Sum('questionvotes__up_vote')).annotate(downvotes=Sum('questionvotes__down_vote')).order_by('-upvotes', 'downvotes')
				response.update({'status':'Most Voted Questions'})
				response.update({'most_voted':True})
			elif sort_by == 'most_viewed':
				questions  = Question.objects.filter(approved=True).annotate(views=Count('questionview')).order_by('-views')
				response.update({'status':'Most Viewed Questions'})
				response.update({'most_viewed':True})
			elif sort_by == 'oldest':
				questions = Question.objects.filter(approved=True).order_by('pk')
				response.update({'status':'Oldest Questions'})
				response.update({'oldest':True})
			else:
				questions = Question.objects.filter(approved=True).order_by('-updated_on')
		else:
			questions = Question.objects.filter(approved=True).order_by('-updated_on')
			response.update({'count':questions.count()})

		page = 1
		if 'page' in request.GET and request.GET['page']:
			page = request.GET['page']
		questions = pagination(questions, page)
			
		response.update({'questions':questions})
		url = request.get_full_path().split('&')
		if url[0] == request.get_full_path():
			url = request.get_full_path().split('?')
			url[0] = url[0] + '?'
		else:
			url[0] = url[0] + '&'
		response.update({'url':url[0]})
		return render_to_response('forum/index.html', response)

def user(request):
	response = {}
	response.update(csrf(request))
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	return render_to_response('forum/user.html', response)


def user_delete_question(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'question' in request.GET and request.GET['question']:
		question_id = request.GET['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, id=question_id)

	if not question.created_by == request.user:
		raise Http404()

	question.delete()

	return HttpResponse('ok')

def user_delete_answer(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'answer' in request.GET and request.GET['answer']:
		answer_id = request.GET['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, id=answer_id)

	if not answer.answered_by == request.user:
		raise Http404()

	answer.delete()

	return HttpResponse('ok')

def user_delete_comment(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'comment' in request.GET and request.GET['comment']:
		comment_id = request.GET['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, id=comment_id)

	if not comment.commented_by == request.user:
		raise Http404()

	comment.delete()

	return HttpResponse('ok')

def user_edit_question(request, pk):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	question = get_object_or_404(Question, pk=pk)
	response.update({'question':question})

	if request.method == 'GET':
		return render_to_response('user_edit_question.html', response)
	
	form_error = False
	if 'title' in request.POST and request.POST['title']:
			title = request.POST['title']
	else:
			response.update({'title_error':True})
			form_error = True

	if 'description' in request.POST and request.POST['description']:
			description = request.POST['description']
	else:
			response.update({'description_error':True})
			form_error = True

	if form_error:
			response.update({'title':request.POST['title']})
			response.update({'description':request.POST['description']})
			response.update({'form_error':True})
			return render_to_response('forum/user_edit_question.html', response)

	question.title = title
	question.description = description
	question.created_by = request.user
	question.slug = slugify(title)
	question.save()

	question.questiontag_set.all().delete()

	tags = ''
	if 'tags' in request.POST and request.POST['tags']:
		tags = request.POST['tags']

	if tags:
		tags = tags.split(',')
		for tag in tags:
			try:
				tagg = Tag.objects.get(slug=slugify(tag))
			except:
				tagg = Tag.objects.create(tag=tag, slug=slugify(tag))
			
			QuestionTag.objects.create(question=question, tag=tagg)


	response.update({'success':True})
	return render_to_response('forum/user_edit_question.html', response)


def user_edit_answer(request):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	response.update({'answer':True})

	if 'answer_id' in request.POST and request.POST['answer_id']:
		answer_id = request.POST['answer_id']
		response.update({'answer_id':answer_id})
	else:
		response.update({'error':True})
		return render_to_response('forum/user.html', response)

	if 'answer' in request.POST and request.POST['answer']:
		answer_content = request.POST['answer']
	else:
		response.update({'error':True})
		return render_to_response('forum/user.html', response)

	answer = get_object_or_404(Answer, pk=answer_id)

	answer.answer = answer_content
	answer.save()

	return render_to_response('forum/user.html', response)

def user_edit_comment(request):
	response = {}

	if 'comment_id' in request.POST and request.POST['comment_id']:
		comment_id = request.POST['comment_id']
	else:
		raise Http404()

	if 'comment' in request.POST and request.POST['comment']:
		comment_data = request.POST['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, pk=comment_id)
	comment.comment = comment_data
	comment.save()
	return HttpResponse('ok')

def users(request):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update({'next':request.get_full_path()})
	response.update({'users':User.objects.filter(is_staff=False, is_superuser=False).order_by('pk')[:20]})
	return render_to_response('forum/users.html', response)

def userdetails(request, pk):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update({'next':request.get_full_path()})
	user = get_object_or_404(User, pk=pk)
	response.update({'userdetails':user})
	response.update({'questions':Question.objects.filter(created_by=user, approved=True)[:10]})
	response.update({'answers':Answer.objects.filter(answered_by=user, approved=True).order_by('-pk')[:10]})
	return render_to_response('forum/userdetails.html', response)


def about(request):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update({'next':request.get_full_path()})
	return render_to_response('forum/about.html', response)

def get_answer(request):
	response = {}
	if 'answer' in request.GET and request.GET['answer']:
		answer_id = request.GET['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, id=answer_id)
	return HttpResponse(answer.answer)

def loadmore_users(request):
	response = {}
	if 'next_rows' in request.GET and request.GET['next_rows']:
		next_rows = request.GET['next_rows']
	else:
		raise Http404()

	users = User.objects.filter(is_staff=False, is_superuser=False).order_by('pk')
	next_row = int(next_rows)
	end_row = next_row + 20
	users = users[next_row:end_row]
	response.update({'users':users})
	if not users:
		return HttpResponse('False')
	else:
		return render_to_response('forum/ajax_users.html',response)

def get_tags(request):
	response = {}
	result = []
	tags = Tag.objects.all()
	for tag in tags:
		result.append(tag.tag) 
	return HttpResponse(
		json.dumps(
			result
		),
		content_type = 'application/json'
  )

def ask_question(request): 
		response = {}
		response.update(csrf(request))

		response.update({'next':request.get_full_path()})
		response.update({'not_authenticated':check_auth(request)})
		response.update({'user':request.user})

		if request.method == 'GET':
				return render_to_response('forum/ask_question.html', response)

		form_error = False
		if 'title' in request.POST and request.POST['title']:
				title = request.POST['title']
		else:
				response.update({'title_error':True})
				form_error = True

		if 'description' in request.POST and request.POST['description']:
				description = request.POST['description']
		else:
				response.update({'description_error':True})
				form_error = True

		if form_error:
				response.update({'title':request.POST['title']})
				response.update({'description':request.POST['description']})
				response.update({'form_error':True})
				return render_to_response('forum/ask_question.html', response)


		if not slugify(title):
			slug = "malayalam"
		else:
			slug = slugify(title)
			
		q = Question.objects.create(title=title, description=description, created_by=request.user, slug=slug)

		tags = ''
		if 'tags' in request.POST and request.POST['tags']:
			tags = request.POST['tags']

		if tags:
			tags = tags.split(',')
			for tag in tags:
				try:
					tagg = Tag.objects.get(slug=slugify(tag))
				except:
					tagg = Tag.objects.create(tag=tag, slug=slugify(tag))
				
				QuestionTag.objects.create(question=q, tag=tagg)


		response.update({'success':True})
		return render_to_response('forum/ask_question.html', response)


def view_question(request, pk, slug):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))

	response.update({'qCount':Question.objects.filter(approved=True).count()})
	response.update({'aCount':Answer.objects.filter(approved=True).count()})
	response.update({'tags':Tag.objects.all()})

	question = get_object_or_404(Question, pk=pk)

	if question.created_by == request.user:
		response.update({'moderator':True})

	if request.user.is_staff:
		response.update({'moderator':True})

	# Question View Count
	if not check_auth(request):
		try:
			QuestionView.objects.create(question=question, user=request.user)
		except:
			pass
	else:
		try:
			QuestionView.objects.create(question=question)
		except:
			pass
	
	response.update({'question':question})
	return render_to_response('forum/view_question.html', response)


def submit_answer(request):
	response = {}

	if 'question' in request.POST and request.POST['question']:
		question_id = request.POST['question']
	else:
		raise Http404()

	if 'answer' in request.POST and request.POST['answer']:
		answer = request.POST['answer']
	else:
		return HttpResponse('empty')

	question = get_object_or_404(Question, pk=question_id)
	
	answer = Answer.objects.create(question=question, answer=answer, answered_by=request.user)
	response.update({'answer':answer})
	return render_to_response('forum/ajax_answer_submit.html', response)

def submit_question_comment(request):
	response = {}
	if 'question' in request.POST and request.POST['question']:
		question_id = request.POST['question']
	else:
		raise Http404()

	if 'comment' in request.POST and request.POST['comment']:
		comment = request.POST['comment']
	else:
		return HttpResponse('empty')

	question = get_object_or_404(Question, pk=question_id)

	comment = Comment.objects.create(question=question, comment=comment, commented_by=request.user)
	response.update({'comment':comment})
	return render_to_response('forum/ajax_comment_submit.html', response)

def submit_answer_comment(request):
	response = {}
	if 'answer' in request.POST and request.POST['answer']:
		answer_id = request.POST['answer']
	else:
		raise Http404()

	if 'comment' in request.POST and request.POST['comment']:
		comment = request.POST['comment']
	else:
		return HttpResponse('empty')

	answer = get_object_or_404(Answer, pk=answer_id)

	comment = Comment.objects.create(answer=answer, comment=comment, commented_by=request.user)
	response.update({'comment':comment})
	return render_to_response('forum/ajax_comment_submit.html', response)

def question_vote(request):
	response = {}
	if 'question' in request.POST and request.POST['question']:
		question_id = request.POST['question']
	else:
		raise Http404()

	if 'vote' in request.POST and request.POST['vote']:
		user_vote = request.POST['vote']
	else:
		raise Http404()

	question = get_object_or_404(Question, pk=question_id)
	if question.created_by == request.user:
		return HttpResponse('no')

	try:
		vote = QuestionVotes.objects.get(question=question, voted_by=request.user)
	except:
		if user_vote == 'up':
			QuestionVotes.objects.create(question=question, voted_by=request.user, up_vote=True)
		else:
			QuestionVotes.objects.create(question=question, voted_by=request.user, down_vote=True)
	else:
		if user_vote == 'up':
			if vote.up_vote and vote.down_vote:
				vote.down_vote = False
			elif vote.up_vote:
				vote.up_vote=False
			else:
				vote.up_vote=True
			vote.save()
		else:
			if vote.up_vote and vote.down_vote:
				pass
			elif vote.down_vote:
				vote.down_vote = False
			else:
				vote.down_vote = True
			vote.save()
	votes = question.getvotescount()
	question.save()
	return HttpResponse(votes)

def answer_vote(request):
	response = {}
	if 'answer' in request.POST and request.POST['answer']:
		answer_id = request.POST['answer']
	else:
		raise Http404()

	if 'vote' in request.POST and request.POST['vote']:
		user_vote = request.POST['vote']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, pk=answer_id)
	if answer.answered_by == request.user:
		return HttpResponse('no')

	try:
		vote = AnswerVotes.objects.get(answer=answer, voted_by=request.user)
	except:
		if user_vote == 'up':
			AnswerVotes.objects.create(answer=answer, voted_by=request.user, up_vote=True)
		else:
			AnswerVotes.objects.create(answer=answer, voted_by=request.user, down_vote=True)
	else:
		if user_vote == 'up':
			if vote.up_vote and vote.down_vote:
				vote.down_vote = False
			elif vote.up_vote:
				vote.up_vote=False
			else:
				vote.up_vote=True
			vote.save()
		else:
			if vote.up_vote and vote.down_vote:
				pass
			elif vote.down_vote:
				vote.down_vote = False
			else:
				vote.down_vote = True
			vote.save()
	votes = answer.getvotescount()
	answer.question.save()
	return HttpResponse(votes)

def question_unanswered(request):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(answer=None, approved=True).distinct()
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Unanswered Questions'})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)

def question_answered(request):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(answer__approved=True).distinct()
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Answered Questions'})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)

def question_resolved(request):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(accepted=True)
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Resolved Questions'})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)

def question_closed(request):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(closed=True)
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Closed Questions'})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)

def tag_questions(request, tag):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(questiontag__tag__slug=slugify(tag))
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Questions tagged with ' + tag})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)


def search_questions(request, search):
	response = {}
	response.update({'next':request.get_full_path()})
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})

	questions = Question.objects.filter(slug__icontains=search)
	response.update({'count':questions.count()})

	page = 1
	if 'page' in request.GET and request.GET['page']:
		page = request.GET['page']
	questions = pagination(questions, page)

	response.update({'questions':questions})
	response.update({'status':'Search results for ' + search})
	response.update({'url':request.get_full_path().split('?')[0] + '?'})
	return render_to_response('forum/index.html', response)

def approve_answer(request):
	response = {}
	if 'answer' in request.POST and request.POST['answer']:
		answer_id = request.POST['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, pk=answer_id)

	if not request.user.is_staff and not answer.question.created_by == request.user:
		return HttpResponse('notAdmin')

	for a in answer.question.answer_set.all():
		a.accepted = False
		a.save()

	answer.accepted = True
	answer.save()
	answer.question.accepted = True
	answer.question.save()

	return HttpResponse('ok')

def question_close(request):
	response = {}
	if 'question' in request.POST and request.POST['question']:
		question_id = request.POST['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, pk=question_id)

	if not request.user.is_staff and question.created_by != request.user:
		return HttpResponse('notAdmin')

	question.closed = True
	question.save()

	return HttpResponse('ok')

def question_reopen(request):
	response = {}
	if 'question' in request.POST and request.POST['question']:
		question_id = request.POST['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, pk=question_id)

	if not request.user.is_staff and question.created_by != request.user:
		return HttpResponse('notAdmin')

	question.closed = False
	question.save()

	return HttpResponse('ok')


def user(request):
	response = {}
	response.update(csrf(request))
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	return render_to_response('forum/user.html', response)


def user_delete_question(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'question' in request.GET and request.GET['question']:
		question_id = request.GET['question']
	else:
		raise Http404()

	question = get_object_or_404(Question, id=question_id)

	if not question.created_by == request.user:
		raise Http404()

	question.delete()

	return HttpResponse('ok')

def user_delete_answer(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'answer' in request.GET and request.GET['answer']:
		answer_id = request.GET['answer']
	else:
		raise Http404()

	answer = get_object_or_404(Answer, id=answer_id)

	if not answer.answered_by == request.user:
		raise Http404()

	answer.delete()

	return HttpResponse('ok')

def user_delete_comment(request):
	response = {}
	if not request.user.is_authenticated():
		raise Http404()

	if 'comment' in request.GET and request.GET['comment']:
		comment_id = request.GET['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, id=comment_id)

	if not comment.commented_by == request.user:
		raise Http404()

	comment.delete()

	return HttpResponse('ok')

def user_edit_question(request, pk):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	question = get_object_or_404(Question, pk=pk)
	response.update({'question':question})

	if request.method == 'GET':
		return render_to_response('forum/user_edit_question.html', response)
	
	form_error = False
	if 'title' in request.POST and request.POST['title']:
			title = request.POST['title']
	else:
			response.update({'title_error':True})
			form_error = True

	if 'description' in request.POST and request.POST['description']:
			description = request.POST['description']
	else:
			response.update({'description_error':True})
			form_error = True

	if form_error:
			response.update({'title':request.POST['title']})
			response.update({'description':request.POST['description']})
			response.update({'form_error':True})
			return render_to_response('forum/user_edit_question.html', response)

	question.title = title
	question.description = description
	question.created_by = request.user
	question.slug = slugify(title)
	question.save()

	question.questiontag_set.all().delete()

	tags = ''
	if 'tags' in request.POST and request.POST['tags']:
		tags = request.POST['tags']

	if tags:
		tags = tags.split(',')
		for tag in tags:
			try:
				tagg = Tag.objects.get(slug=slugify(tag))
			except:
				tagg = Tag.objects.create(tag=tag, slug=slugify(tag))
			
			QuestionTag.objects.create(question=question, tag=tagg)


	response.update({'success':True})
	return render_to_response('forum/user_edit_question.html', response)


def user_edit_answer(request):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update(csrf(request))
	response.update({'answer':True})

	if 'answer_id' in request.POST and request.POST['answer_id']:
		answer_id = request.POST['answer_id']
		response.update({'answer_id':answer_id})
	else:
		response.update({'error':True})
		return render_to_response('forum/user.html', response)

	if 'answer' in request.POST and request.POST['answer']:
		answer_content = request.POST['answer']
	else:
		response.update({'error':True})
		return render_to_response('forum/user.html', response)

	answer = get_object_or_404(Answer, pk=answer_id)

	answer.answer = answer_content
	answer.save()

	return render_to_response('forum/user.html', response)

def user_edit_comment(request):
	response = {}

	if 'comment_id' in request.POST and request.POST['comment_id']:
		comment_id = request.POST['comment_id']
	else:
		raise Http404()

	if 'comment' in request.POST and request.POST['comment']:
		comment_data = request.POST['comment']
	else:
		raise Http404()

	comment = get_object_or_404(Comment, pk=comment_id)
	comment.comment = comment_data
	comment.save()
	return HttpResponse('ok')

def users(request):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update({'next':request.get_full_path()})
	response.update({'users':User.objects.filter(is_staff=False, is_superuser=False).order_by('pk')[:20]})
	return render_to_response('forum/users.html', response)

def userdetails(request, pk):
	response = {}
	response.update({'not_authenticated':check_auth(request)})
	response.update({'user':request.user})
	response.update({'next':request.get_full_path()})
	user = get_object_or_404(User, pk=pk)
	response.update({'userdetails':user})
	response.update({'questions':Question.objects.filter(created_by=user, approved=True)[:10]})
	response.update({'answers':Answer.objects.filter(answered_by=user, approved=True).order_by('-pk')[:10]})
	return render_to_response('forum/userdetails.html', response)
