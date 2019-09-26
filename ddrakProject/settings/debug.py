from .base import *

'''
Used when debugging by local server.
to run localhost: python(3) manage.py runserver
difference from deploy: 1. DEBUG is True
                        2. STATICFILES_DIRS instead of STATIC_ROOT
                        ** STATIC_ROOT and STATICFILES_DIRS cannot be dupplicated!!
'''

DEBUG = True
STATICFILES_DIRS = (
    # There should be ','!!
    os.path.join(PROJECT_PATH, 'assets'),
)

WSGI_APPLICATION = 'ddrakProject.wsgi.debug.application'
