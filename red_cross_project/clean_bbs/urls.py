from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", 'red_cross_project.clean_bbs.views.bbs', name="bbs"),
    url(r"^page/(?P<page_index>\d+)/$", 'red_cross_project.clean_bbs.views.bbs', name="bbs_page_index"),
    url(r"^post/$",'red_cross_project.clean_bbs.views.post', name="post_question"),
    url(r"^edit/(?P<question_id>\d+)/$",'red_cross_project.clean_bbs.views.edit', name="edit_question"),
    url(r"^delete/(?P<question_id>\d+)/$",'red_cross_project.clean_bbs.views.delete', name="delete_question"),
    url(r"^(?P<question_id>\d+)/$",'red_cross_project.clean_bbs.views.single', name="single_question"),
)
