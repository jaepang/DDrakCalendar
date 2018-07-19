"""
WSGI config for lala project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ddrakProject.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
