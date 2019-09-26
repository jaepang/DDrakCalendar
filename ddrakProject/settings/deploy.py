from .base import *
import dj_database_url
from whitenoise.django import DjangoWhiteNoise

'''
Used when deploying by heroku.
to deploy (on heroku): push github and just press "deploy branch" button.
difference from debug: 1. DEBUG is False
                       2. STATIC_ROOT instead of STATICFILES_DIRS.
                       ** STATIC_ROOT and STATICFILES_DIRS cannot be dupplicated!!
                       3. database setting for heroku exists.
'''

DEBUG = False
STATIC_ROOT = os.path.join(PROJECT_PATH, 'assets')

WSGI_APPLICATION = 'ddrakProject.wsgi.deploy.application'
WSGI_APPLICATION = DjangoWhiteNoise(WSGI_APPLICATION)

# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
