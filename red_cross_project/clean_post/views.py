#coding=utf-8

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from red_cross_project.clean_post.models import *
from red_cross_project.forms import SearchForm
from red_cross_project.clean_post.forms import *
from red_cross_project.woosh_searcher import Searcher

# Create your views here.
def posts(request, **kwargs):
	total_set = []
	debug = []
	#get the  list to render
	if request.method == 'GET':
		if 'search' in request.GET:
			search_form = SearchForm(request.GET)
			if search_form.is_valid():
				cd = search_form.cleaned_data
				keywords = cd['key_words']
				if keywords is None:
					total_set = Post.objects.order_by('-update_time')
				else:
					#start to search for posts and replies using whoosh 
					searcher = Searcher()
					matching_ids = searcher.search(unicode(keywords),u'post')
					debug.append(unicode(keywords))
					debug.append(matching_ids)
					for id in matching_ids:
						try:
							total_set.append(Post.objects.get(id=id))
						except:
							raise Exception('This post does not exist anymore')
			else:
				total_set = Post.objects.order_by('-update_time')
		else: #no form submited
			total_set = Post.objects.order_by('-update_time')

	total_set_size = len(total_set)
	total_page_number = total_set_size/12+1

	if not kwargs.has_key('page_index')	:
		#when no filter options & search keywords
		posts = total_set[0 : 12]	
		page_index = 1
	else:
		page_index = int(kwargs['page_index'])
		#get the page range to render
		#by default there are 20 pages in one page
		start_idx = 12 * ( page_index - 1) 
		#get the result_set with page nubmer limiting
		posts = total_set[ start_idx : start_idx + 12 ]

	#prepare the context
	context = {'posts':posts}
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

	return render_to_response("posts.html",context,context_instance = RequestContext(request, {}))

def single(request, **kwargs):
	context = {}
	errors = []

	post_id = kwargs['post_id']
	try:
		post = Post.objects.get(id=post_id)
		context['post'] = post 
	except:
		raise Exception("Can not find post with id"+str(post_id))
	if request.method=='POST':
		if 'reply' in request.POST:
			form = ReplyForm(request.POST)
			if form.is_valid():
				reply = form.save(commit=False)
				reply.post = post	
				reply.author = request.user
				reply.title = u'回复：'	+ post.title
				reply.save()

				# add the post to IR index
				searcher = Searcher()
				searcher.add_documents(reply.id,reply.title,reply.content,u'reply')

				try:
					post = Post.objects.get(id=post_id)
					context['post'] = post
					context['form'] = ReplyForm() 
				except:
					raise Exception("Can not find post with id"+str(post_id))
				return render_to_response("single_post.html",context,\
					context_instance = RequestContext(request,{}))
			else:#the form is invalid
				errors.append(u"不好意思，您的回答字数不符合标准。")
				context['errors'] = errors
				return render_to_response("single_post.html", context,\
					context_instance = RequestContext(request, {}))
		else:#
			pass
	else:#no form submited
		context['form'] = ReplyForm(request.POST)
		if request.user.is_authenticated() :
			context['authenticated'] = True 
		else:
			context['authenticated'] = False
		return render_to_response("single_post.html", context,\
			context_instance = RequestContext(request, {}))


@login_required
def new(request, **kwargs):
	context = {}	
	errors = []
	if request.method == "POST":
		if 'post' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				post=form.save(commit=False)	
				post.author = request.user
				post.save()
				# add the post to IR index
				searcher = Searcher()
				searcher.add_documents(post.id,post.title,post.content,u'post')
				return HttpResponseRedirect('/post/')
			else:# form is not valid
				#TODO: various errors
				errors.append(u'对不起,您发表的字数超啦')
				context['form'] = form
				context['errors'] = errors
				return render_to_response('edit_post.html',context,context_instance=RequestContext(request, {}))
		else:
			raise Exception("not good")
	else:
		context['form'] = PostForm(request.POST)
		return render_to_response('edit_post.html',context, context_instance=RequestContext(request, {}))

#login_required
def delete(request,**kwargs):
	#find the previous post with post_id
	try:
		post = Post.objects.get(id=kwargs['post_id'])
	except:
		raise Http404
	#if the user is the author of this quesiton	
	if request.user.id == post.author.id:
		post.delete()
		#delete the IR index
		searcher = Searcher()
		searcher.delete_document(post.id,'post')
	return HttpResponseRedirect('/bbs/')

@login_required
def edit(request,**kwargs):
	context = {}	
	errors = []
	#find the previous post with post_id
	try:
		post = Post.objects.get(id=kwargs['post_id'])
	except:
		raise Http404
	if request.method == "POST":
		if 'post' in request.POST:
			form = PostForm(request.POST)
			if form.is_valid():
				new_post = form.save(commit=False)	
				post.title = new_post.title
				post.content = new_post.content
				post.save()

				searcher = Searcher()
				#update the index 
				searcher.update_document(post.id,post.title,post.content,u'post')
				return HttpResponseRedirect('/bbs/')
			else:# form is not valid
				#TODO: various errors
				errors.append(u'对不起,您发表的问题字数超啦')
				context['form'] = form
				context['errors'] = errors
				return render_to_response('edit_post.html',context,context_instance=RequestContext(request, {}))
		else:
			raise Http404	
	else:
		#fill the form
		context['form'] = PostForm(instance=post)
		return render_to_response('edit_post.html',context, context_instance=RequestContext(request, {}))
