from .base import *
import dj_database_url
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

DEBUG = False
WSGI_APPLICATION = get_wsgi_application()
WSGI_APPLICATION = DjangoWhiteNoise(WSGI_APPLICATION)


# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
