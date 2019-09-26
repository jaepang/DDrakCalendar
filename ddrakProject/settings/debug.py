from .base import *

'''
Used when debugging by local server.
to run localhost: python(3) manage.py runserver
difference from deploy: DEBUG is True
'''

DEBUG = True

WSGI_APPLICATION = 'ddrakProject.wsgi.debug.application'
