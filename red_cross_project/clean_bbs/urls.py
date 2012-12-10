from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "bbs.html"}, name="bbs"),
    url(r"^post/$",'red_cross_project.clean_bbs.post',name="post"),
)
