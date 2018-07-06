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
    url(r'^SetTime/', TemplateView.as_view(template_name="SetTime.html"), name='setTime'),
    url(r'^LFDMtimetable/', views.LFDM, name='LFDM'),
    url(r'^MMGEtimetable/', views.MMGE, name='MMGE'),
    url(r'^MYRtimetable/', views.MYR, name='MYR'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
