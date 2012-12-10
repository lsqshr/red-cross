from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from red_cross_project.clean_bbs import urls

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from .views import SignupView


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
    url(r"^bbs/", include("red_cross_project.clean_bbs.urls")),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
