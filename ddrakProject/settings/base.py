import os
from django.core.exceptions import ImproperlyConfigured

# http->https redirection is at web server layer (nginx)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SECRET KEY is saved in Heroku config variable (deploy environment)
#                           And local  variable (development environment)
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable("SECRET_KEY")

PROJECT_PATH = os.path.realpath((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

ADMINS = (
    ('ShinJaekwang', 'shinjawkwang@naver.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'postgresql-fluffy-33003.c4gwnuxfdohi.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
        'NAME': 'postgresql_fluffy_33003',
        'USER': 'lfdm',
        'PASSWORD': 'thirtytwo2521',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['ddrakcalendar.herokuapp.com', 'ddrakcalendar.com', 'ec2-13-125-142-67.ap-northeast-2.compute.amazonaws.com']

TIME_ZONE = 'Asia/Seoul'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False

MEDIA_ROOT = PROJECT_PATH + '/media/'
MEDIA_URL = ''
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# List of callables that know how to import templates from various sources.
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'ddrakProject.urls'

# Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'ddrakProject.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'rest_framework',
    'rest_framework_swagger',
    'debug_toolbar',
    'djangobower',
    'schedule',
    'ddrakProject',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

BOWER_INSTALLED_APPS = (
    'jquery',
    'jquery-ui',
    'bootstrap',
    'fullcalendar'
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_PATH, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.request',
        ],
    },
}]

# Auth settings
LOGIN_REDIRECT_URL = '/timetable/'
