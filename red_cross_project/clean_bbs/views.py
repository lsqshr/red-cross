from django.shortcuts import render_to_response
from red_cross_project.clean_bbs.models import Question,Answer


def bbs(request):

	#get the question list to render
	#TODO:deal with the filter
	#when no filter options & search keywords
	questions = Question.objects.all()

	context = {'questions':questions}
	return render_to_response("bbs.html",context)

@login_required
def post(request):
	context = {'form': form}	
	errors = []
	if request.method == "POST":
		if 'question' in request.POST:
			form = QuestionForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				title=cd['title']
				content=cd['content']
			else:# form is not valid
				#TODO: various errors
				errors.append(u'对不起,您发表的问题字数超啦')
				context['errors'] = errors
				return render_to_response('post.html',context)
