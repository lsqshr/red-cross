from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", 'red_cross_project.clean_post.views.posts', name="posts"),
    url(r"^new/$", 'red_cross_project.clean_post.views.new', name="new_post"),
    url(r"^page/(?P<page_index>\d+)/$", 'red_cross_project.clean_post.views.posts', name="post_page_index"),
    url(r"^(?P<post_id>\d+)/$",'red_cross_project.clean_post.views.single', name="single_post"),
    url(r"^edit/(?P<post_id>\d+)/$",'red_cross_project.clean_post.views.edit', name="edit_post"),
    url(r"^delete/(?P<post_id>\d+)/$",'red_cross_project.clean_post.views.delete', name="delete_post"),
)
