from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.Initialize, name='home'),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^timetable/', TemplateView.as_view(template_name="timetable.html"), name='timetable'),
    url(r'^SetTime/', views.SetTime, name='setTime'),
    url(r'^StayAwake/', views.StayAwake, name='stayAwake'),
    url(r'^StayAwakeError/', TemplateView.as_view(template_name="StayAwakeError.html"),name='stayAwakeError'),
    url(r'^SetClubTime/', views.IndividualTimeSet, name='individualTimeSet'),
    url(r'^ClubSubmit/$', views.clubSubmit, name='ClubSubmit'),
    url(r'^ClubTimeError/', TemplateView.as_view(template_name="IndividualTimeSetError.html"),name='timeSetError'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^awsubmit/$', views.awakeSubmit, name='awsubmit'),
    url(r'^DeleteEvent/', views.delete, name='DeleteEvent'),
    url(r'^LFDMtimetable/', views.LFDM, name='LFDM'),
    url(r'^MMGEtimetable/', views.MMGE, name='MMGE'),
    url(r'^MYRtimetable/', views.MYR, name='MYR'),
    url(r'^permission/',TemplateView.as_view(template_name="InvalidPermission.html"), name='permission'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^password/', views.change_password, name='change_password'),
    url(r'^result/', views.change_check, name='change_result'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
