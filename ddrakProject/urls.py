from django.views.generic import TemplateView
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib.auth import views as auth_views
from . import views

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.init, name='home'),
    url(r'^timetable/', TemplateView.as_view(template_name="timetable.html"), name='timetable'),
    
    url(r'^stime/', views.set_time, name='setTime'),
    url(r'^sctime/', views.set_time_club, name='set_time_club'),
    url(r'^allnight/', views.allnight, name='allnight'),
    url(r'^borrow/', views.borrow, name='borrow'),
    
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^subborrow/$', views.borrowSubmit, name='borrow_submit'),
    url(r'^subclub/$', views.clubSubmit, name='clubSubmit'),
    url(r'^allsubmit/$', views.allnight_submit, name='allnight_submit'),
    
    url(r'^delete/', views.delete, name='delete'),
    
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^password/', views.change_password, name='change_password'),
    url(r'^result/', views.change_check, name='change_result'),
    
    url(r'^error/',TemplateView.as_view(template_name="error.html"), name='error'),
]

handler400 = 'ddrakProject.views.bad_request'
handler403 = 'ddrakProject.views.permission_denied'
handler404 = 'ddrakProject.views.page_not_found'
handler500 = 'ddrakProject.views.server_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
