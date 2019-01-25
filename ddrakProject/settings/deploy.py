from .base import *
import dj_database_url
from whitenoise.django import DjangoWhiteNoise

DEBUG = False
WSGI_APPLICATION = 'ddrakProject.wsgi.deploy.application'

WSGI_APPLICATION = DjangoWhiteNoise(WSGI_APPLICATION)
