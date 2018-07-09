from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="homepage.html"),),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^timetable/', TemplateView.as_view(template_name="timetable.html"), name='timetable'),
    url(r'^SetTime/', views.SetTime, name='setTime'),
    url(r'^submit1/$', views.submit1, name='subit1'),
    url(r'^submit2/$', views.submit2, name='subit2'),
    url(r'^submit3/$', views.submit3, name='subit3'),
    url(r'^LFDMtimetable/', views.LFDM, name='LFDM'),
    url(r'^MMGEtimetable/', views.MMGE, name='MMGE'),
    url(r'^MYRtimetable/', views.MYR, name='MYR'),
    url(r'^permission/',TemplateView.as_view(template_name="InvalidPermission.html"), name='permission'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
