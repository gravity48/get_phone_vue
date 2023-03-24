"""
Django settings for get_phone_view project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from datetime import timedelta
import copy
import os
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext_lazy as _
from loguru import logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$_^=a(ygl5+ydc&&ly9fb7li#m-zpu)9bz%1mag7a7xut@w+k5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

# Application definition

INSTALLED_APPS = [
    'index.apps.IndexConfig',
    'searchnumber.apps.SearchnumberConfig',
    'osa_settings.apps.OsaSettingsConfig',
    'searchfio.apps.SearchfioConfig',
    'custom_auth.apps.CustomAuthConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'api.apps.ApiConfig',
    'django_filters',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'get_phone_view.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'get_phone_view.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASE_ROUTERS = ['get_phone_view.routers.OsaExtraRouter',
                    'get_phone_view.routers.DefaultRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'search_numbers',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '172.17.0.1',
        'PORT': '5432',
    },
    'osa_extra': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'osa_extra',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '172.17.0.1',
        'PORT': '5432',
    }
}
# Cashes
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'all',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',

    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
   # 'EXCEPTION_HANDLER': 'api.utils.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(minutes=5),
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATICFILES_DIRS = [
    ("", os.path.join(BASE_DIR, "assets/")),
]


STATIC_URL = '/assets/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = '/media/'


MAX_UPLOAD_SIZE = 100000000

DEFAULT_FILE_STORAGE = FileSystemStorage(location=f'{BASE_DIR}/logfiles')

SUCCESS_STATUS = 200
ERROR_STATUS = 404

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

LOGGER = logger

LOGGER.add(f'{BASE_DIR}/logfiles/get_phone.txt', format='{time} {level} {message}', level='DEBUG', rotation='500kb', compression='zip')

TEMP_DIR = f'{BASE_DIR}/temp'

LOGIN_URL = 'auth/'

TRAINING_PATH = '/mnt/'

CELERY_BROKER_USER = 'user_m'

CELERY_BROKER_PASSWORD = '000092'

CELERY_BROKER_HOST = '172.17.0.1'

CELERY_BROKER_PORT = 5672

DEF_ERROR_MESSAGES = {
    'invalid': _('Проверьте корректность поля'),
    'required': _('Поле обязательно к заполнению'),
    'null': _('Поле не может быть пустым'),
    'unique': _('Поле должно быть уникальным'),
    'blank': _('Поле не может быть пустым'),

}

