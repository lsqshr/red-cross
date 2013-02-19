from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

from red_cross_project.clean_bbs import urls

urlpatterns = patterns("",
    url(r"^$", 'red_cross_project.views.homepage', name="home"),
    url(r"^admin/", include(admin.site.urls)),
    #url(r"^accounts/signup/$",'red_cross_project.views.signup' , name="account_signup"),
    url(r"^accounts/login/$",'red_cross_project.views.login', name='login'),
    url(r"^accounts/profile_settings/$", 'red_cross_project.views.profile_settings', name="profile_settings"),
    url(r"^accounts/", include("account.urls")),
    url(r"^bbs/", include("red_cross_project.clean_bbs.urls")),
    url(r"^post/", include("red_cross_project.clean_post.urls")),
    url(r"^guide/",'red_cross_project.views.guide',name="guide"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
