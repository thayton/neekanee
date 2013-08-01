import os
import socket

PRODUCTION_WEB_SERVER_IP = '69.164.219.250'

# Django settings for jobsearch project.

if socket.gethostbyname(socket.gethostname()) == PRODUCTION_WEB_SERVER_IP:
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
else:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

#SESSION_COOKIE_SECURE = True

ADMINS = (
    ('Todd H', 'thayton@neekanee.com'),
)

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'thayton'
EMAIL_HOST_PASSWORD = 'lgehltb69'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'feedback@neekanee.com'
SERVER_EMAIL = 'feedback@neekanee.com'

# django-allauth settings
#ACCOUNT_AUTHENTICATION_METHOD = 'email'
#ACCOUNT_USERNAME_REQUIRED = False
#ACCOUNT_EMAIL_REQUIRED = True
#ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/account/email/'
ACCOUNT_USER_DISPLAY = 'neekanee_solr.views.user_display'

MANAGERS = ADMINS

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/profile/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'neekanee_solr',              # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'lgehltb69',              # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/Users/thayton/Projects/Mine/jobsearch/neekanee_solr/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'neekanee_solr/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
if socket.gethostbyname(socket.gethostname()) == PRODUCTION_WEB_SERVER_IP:
    MEDIA_URL = 'http://www.neekanee.com/media/'
else:
    MEDIA_URL = 'http://127.0.0.1:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
#STATIC_URL = '/static/'
STATIC_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dsli$cxwddfo(m*3iek(7(4um$ktk11!@9p!go#*2f_t@3)a08'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'neekanee.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'neekanee_solr/templates/')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    'neekanee_solr',
    'bootstrapform',
    'uni_form',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.linkedin',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'neekanee_solr.context_processors.get_current_path',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'neekanee_solr/fixtures/'),
)
