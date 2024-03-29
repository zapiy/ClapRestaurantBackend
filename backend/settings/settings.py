"""
Django settings for neuroezotericabackend project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from urllib.parse import urlparse
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", None, cast=str)

DEBUG = config("DEBUG", default=True, cast=bool)

USE_SECURE_HTTPS = config("USE_SECURE_HTTPS", default=False, cast=bool)
if not USE_SECURE_HTTPS:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INTERNET_URL = config("INTERNET_URL", default='http://127.0.0.1:8000')
PRODUCTION_DATABASE = config("PRODUCTION_DATABASE", cast=bool, default=False)
INTERNET_DOMAIN = urlparse(INTERNET_URL).netloc

APPEND_SLASH=False

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ORIGIN = ["*"]
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
CORS_ALLOW_HEADERS = ["*"]
# CORS_ALLOW_HEADERS = [
#     "Accept", "Origin",
#     "Content-Type",
#     "X-Requested-With",
#     "Authorization",
#     "x-csrf-token"
# ]

ASGI_APPLICATION = 'settings.asgi.application'
WSGI_APPLICATION = 'settings.wsgi.application'

INSTALLED_APPS = [
    'cdn.apps.Config',
    'mobile.apps.Config',
    'admin.apps.Config',
    'daphne',
    
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [    
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.CrossOriginHeaderMiddleware',
    'middleware.ContentTypeConverterMiddleware',
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'admin.middleware.context_processors.permission_helper',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

if PRODUCTION_DATABASE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': '3N3jTNG0ovMRXf15i9t1fupdHBda63m7MNXPf6cWr2sdhFHf0J',
            'HOST': 'postgres',
            'PORT': '5432',
            'OPTIONS': {'sslmode': 'disable'},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Internationalization
LANGUAGE_CODE = 'en-EN'

USE_I18N = True
USE_TZ = PRODUCTION_DATABASE

TIME_FORMAT = "%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = None
AUTH_USER_MODEL = ""

SESSION_COOKIE_AGE = timedelta(days=30).total_seconds()

if USE_SECURE_HTTPS:
    SESSION_COOKIE_SAMESITE = ""
    SESSION_COOKIE_SECURE = True

# Static files

MEDIA_URL = "/cdn/"
MEDIA_ROOT = BASE_DIR / "stored"

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# 3-Party

GMAIL_CREDS = config(
    "GMAIL_CREDS", default=None,
    cast=lambda v: None if v is None else str(v).partition(':')[::2]
)
