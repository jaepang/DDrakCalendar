"""
WSGI config

set default setting mode and run get_wsgi_application()

deploy: ddrakProject.settings.deploy
debug : ddrakProject.settings.debug
"""

import os
from django.core.wsgi import get_wsgi_application

# This is important!!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ddrakProject.settings.deploy")

application = get_wsgi_application()
