#coding=utf-8
from red_cross_project.woosh_searcher import Searcher
import sys

s = Searcher()
s.create_schema()
s.add_all_questions_and_answers()
print s.search(u'很重',u'question')
