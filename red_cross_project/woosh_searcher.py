#coding=utf-8
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
from red_cross_project.clean_bbs.models import Question,Answer

class Searcher(object):
	ix = None
	index_dir = "red_cross_project/site_media/index"

	def create_schema(self):
		analyzer = RegexAnalyzer(ur"([\u4e00-\u9fa5])|(\w+(\.?\w+)*)")  
		#index_id is formated as 'question14'
		schema = Schema(index_id = ID(unique=True),id=NUMERIC(stored=True),\
			title=TEXT(stored=True), content=TEXT(analyzer=analyzer), type=TEXT)
		if not os.path.exists(self.index_dir):
		    os.mkdir(self.index_dir)
		self.ix = create_in(self.index_dir, schema)

	def add_all_questions_and_answers(self):
		if not self.ix:
			self.ix = self._open_index()
		writer = self.ix.writer()
		questions = Question.objects.all()
		for question in questions:
			writer.add_document(index_id=u'question'+unicode(str(question.id)),\
			 id=question.id,title=question.title,\
			 content=question.content,type=u'question')
		answers = Answer.objects.all()
		for answer in answers:
			writer.add_document(index_id=u'answer'+unicode(str(answer.id)),id=answer.id,title=answer.title,\
			 content=answer.content,type=u'answer')

		writer.commit()

	def add_all_posts_and_replies(self):
		pass

	def add_documents(self,id,title,content,type):
		if self.ix is None:
			self.ix = self._open_index()
		writer = self.ix.writer()
		writer.add_document(index_id=type+str(id),id=id,title=title, content=content,type=type)
		writer.commit(merge = True, optimize = True)

	def _open_index(self):
		return open_dir(self.index_dir)

	def _prepare_query(self,keywords,type):
		if self.ix is None:
			self.ix = self._open_index()
		parser = QueryParser(u"content", self.ix.schema)
		return parser.parse(keywords+u" AND (type:"+type+")")
		#return parser.parse(keywords)

	def delete_document(self,id,type):
		if self.ix is None:
			self.ix = self._open_index()
		writer = self.ix.writer()
		writer.delete_by_term('id', unicode(type+str(id)))
		writer.commit(merge = True, optimize = True)

	def update_document(self,id,title,content,type):
		if self.ix is None:
			self.ix = self._open_index()
		writer = self.ix.writer()
		writer.update_document(index_id=type+str(id),id=id,title=title, content=content,type=type)
		writer.commit(merge = True, optimize = True)

	def search(self,keywords,type):
		'''
		take in the searching keywords and returns 
		a list of question id with ordering
		'''
		if self.ix is None:
			self.ix = self._open_index()
		print 'in searching...\n'
		id_list = []
		query = self._prepare_query(keywords,type)
		#print query
		with self.ix.searcher() as searcher:
			result = searcher.search(query)
			print result
			for r in result:
				id_list.append(r['id'])

		return id_list
