#coding=utf-8

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from red_cross_project.clean_bbs.models import Question,Answer
from red_cross_project.clean_bbs.forms import *

import datetime

def bbs(request, **kwargs):
	total_set = []
	debug = []
	context = {}
	#get the question list to render
	if request.method == 'GET':
		total_set = Question.objects.order_by('-update_time')


	total_set_size = len(total_set)
	total_page_number = total_set_size/12+1

	if not kwargs.has_key('page_index')	:
		#when no filter options & search keywords
		questions = total_set[0 : 12]	
		page_index = 1
	else:
		page_index = int(kwargs['page_index'])
		#get the page range to render
		#by default there are 20 pages in one page
		start_idx = 12 * ( page_index - 1) 
		#get the result_set with page nubmer limiting
		questions = total_set[ start_idx : start_idx + 12 ]

	#prepare the context
	context['request'] = request
	context['questions'] = questions
	context['cur_index'] = page_index
	if page_index is 1:
		context['last_index'] = 1
	else:
		context['last_index'] = page_index-1
	if page_index is total_page_number:
		context['next_index'] = total_page_number 
	else:
		context['next_index'] = page_index+1
	context['total_set_size'] = total_set_size
	context['total_page_number'] = total_page_number

	context['page_name'] = 'bbs'

	return render_to_response("bbs.html",context,context_instance = RequestContext(request, {}))


def single(request, **kwargs):
	context = {}
	errors = []

	context['page_name'] = 'bbs'
	question_id = kwargs['question_id']
	try:
		question = Question.objects.get(id=question_id)
		context['question'] = question
	except:
		raise Exception("Can not find question with id"+str(question_id))
	if request.method=='POST':
		if 'answer' in request.POST and request.user.is_authenticated():
			context['authenticated'] = True
			form = AnswerForm(request.POST)
			if form.is_valid():
				answer = form.save(commit=False)
				answer.question = question	
				answer.author = request.user
				answer.title = u'回复：'	+ question.title
				answer.save()

				# add the question to IR index
				searcher = Searcher()
				searcher.add_documents(answer.id,answer.title,answer.content,u'answer')

				try:
					question = Question.objects.get(id=question_id)
					context['question'] = question
					context['form'] = AnswerForm() 
				except:
					raise Exception("Can not find question with id "+str(question_id))
				context['answers'] = question.sorted_answers()
				return render_to_response("single.html",context,\
					context_instance = RequestContext(request,{}))
			else:#the form is invalid
				errors.append(u"不好意思，您的回答字数不符合标准。")
				context['errors'] = errors
				return render_to_response("single.html", context,\
					context_instance = RequestContext(request, {}))
		else:#
			HttpResponseRedirect('account_login')
	else:#no form submited
		context['form'] = AnswerForm(request.POST)
		if request.user.is_authenticated() :
			context['authenticated'] = True 
		else:
			context['authenticated'] = False

		return render_to_response("single.html", context,\
			context_instance = RequestContext(request, {}))


def post(request,**kwargs):
	context = {}	
	errors = []
	debug = [] 

	if request.method == "POST":
		form = QuestionForm( request.POST )

		if form.is_valid():
			question = form.save(commit=False)	

			if request.user and request.user.is_authenticated() :
				question.author = request.user
			else :
				question.author = None
			question.update_time = datetime.datetime.now()
			question.post_time = datetime.datetime.now()
			question.save()
			# add the question to IR index
			searcher = Searcher()
			searcher.add_documents( question.id, question.title, question.content, u'question' )

			if request.POST['auth'] == 'False' :
				temp_profile_form = TempProfileForm( request.POST )
				if temp_profile_form.is_valid() :
					debug.append('in valid')
					profile = temp_profile_form.save( commit = False )
					profile.question = question
					profile.save()
				else:
					errors.append(u'对不起，您输入的信息有误')
					context['form'] = form
					context['temp_profile_form'] = TempProfileForm( request.POST )
					context['errors'] = errors
					return render_to_response('post.html',context,\
						context_instance=RequestContext(request, {}))

			context['debug'] = debug
			#return HttpResponse(''.join(debug))
			return HttpResponseRedirect('/bbs/')

		else:# form is not valid
			errors.append(u'对不起,您发表的问题字数超啦')
			context['form'] = form
			context['temp_profile_form'] = TempProfileForm(request.POST)
			context['errors'] = errors
			return render_to_response('post.html',context,\
				context_instance=RequestContext(request, {}))
	else:
		context['form'] = QuestionForm(request.POST)
		context['temp_profile_form'] = TempProfileForm(request.POST)
		return render_to_response('post.html', context, context_instance=RequestContext(request, {}))

#login_required
def delete(request,**kwargs):
	#find the previous question with question_id
	try:
		question = Question.objects.get(id=kwargs['question_id'])
	except:
		raise Http404
	#if the user is the author of this quesiton	
	if request.user.id == question.author.id:
		question.delete()
		#delete the IR index
		searcher = Searcher()
		searcher.delete_document(question.id,'question')
	return HttpResponseRedirect('/bbs/')

@login_required
def edit(request,**kwargs):
	context = {}	
	errors = []
	#find the previous question with question_id
	try:
		question = Question.objects.get(id=kwargs['question_id'])
	except:
		raise Http404
	if request.method == "POST":
		if 'question' in request.POST:
			form = QuestionForm(request.POST)
			if form.is_valid():
				new_question = form.save(commit=False)	
				question.title = new_question.title
				question.content = new_question.content
				question.save()

				searcher = Searcher()
				#update the index 
				searcher.update_document(question.id,question.title,question.content,u'question')
				return HttpResponseRedirect('/bbs/')
			else:# form is not valid
				#TODO: various errors
				errors.append(u'对不起,您发表的问题字数超啦')
				context['form'] = form
				context['errors'] = errors
				return render_to_response('post.html',context,context_instance=RequestContext(request, {}))
		else:pass
	else:
		#fill the form
		context['form'] = QuestionForm(instance=question)
		return render_to_response('post.html',context, context_instance=RequestContext(request, {}))
