#coding=utf-8

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from red_cross_project.clean_bbs.models import Question,Answer
from red_cross_project.clean_bbs.forms import *


def bbs(request, **kwargs):
	#get the question list to render
	#TODO:deal with the filter
	total_set = Question.objects.all()
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
		questions = Question.objects.order_by('update_time')[ start_idx : start_idx + 12 ]

	#prepare the context
	context = {'questions':questions}
	context['search_form'] =  SearchForm()
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

	return render_to_response("bbs.html",context)

def single(request, **kwargs):
	context = {}
	errors = []

	question_id = kwargs['question_id']
	try:
		question = Question.objects.get(id=question_id)
		context['question'] = question
	except:
		raise Exception("Can not find question with id"+str(question_id))
	if request.method=='POST':
		if 'answer' in request.POST:
			form = AnswerForm(request.POST)
			if form.is_valid():
				answer = form.save(commit=False)
				answer.question = question	
				answer.author = request.user
				answer.title = u'回复：'	+ question.title
				answer.save()
				try:
					question = Question.objects.get(id=question_id)
					context['question'] = question
					context['form'] = AnswerForm() 
				except:
					raise Exception("Can not find question with id"+str(question_id))
				return render_to_response("single.html",context,\
					context_instance = RequestContext(request,{}))
			else:#the form is invalid
				errors.append(u"不好意思，您的回答字数不符合标准。")
				context['errors'] = errors
				return render_to_response("single.html", context,\
					context_instance = RequestContext(request, {}))
		else:#
			pass
	else:#no form submited
		context['form'] = AnswerForm(request.POST)
		return render_to_response("single.html", context,\
			context_instance = RequestContext(request, {}))


@login_required
def post(request):
	context = {}	
	errors = []
	if request.method == "POST":
		if 'question' in request.POST:
			form = QuestionForm(request.POST)
			if form.is_valid():
				question=form.save(commit=False)	
				question.author = request.user
				question.save()
				return HttpResponseRedirect('/bbs/')
			else:# form is not valid
				#TODO: various errors
				errors.append(u'对不起,您发表的问题字数超啦')
				context['form'] = form
				context['errors'] = errors
				return render_to_response('post.html',context,context_instance=RequestContext(request, {}))
		else:pass
	else:
		context['form'] = QuestionForm(request.POST)
		return render_to_response('post.html',context, context_instance=RequestContext(request, {}))
