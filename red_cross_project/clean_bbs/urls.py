from django.conf.urls import patterns, include, url

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "bbs.html"}, name="bbs"),
)
