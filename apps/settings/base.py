"""
Django settings for SegmentationCheck project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from unipath import Path
PROJECT_DIR =  Path(__file__).ancestor(3)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'apps'))


import djcelery


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = '7hjHnMmsHduzVfxrf6upTFdhNRBiQunQLaQt'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = [
    '112.74.23.141',
    '127.0.0.1',
    'dzj3000.com',
    'www.dzj3000.com',
]


# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'djcelery',
    'django_slack',
    "compressor",
    'rest_framework_swagger',
    ]

LOCAL_APPS = [
    'home',
    'quiz',
    'account',
    'catalogue',
    'managerawdata',
    'segmentation',
    'characters',
    'classification_statistics',
    'preprocess'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

djcelery.setup_loader()
BROKER_URL = 'redis+socket:///var/run/redis/redis.sock'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_DISABLE_RATE_LIMITS = True

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1'
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.child("templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

WSGI_APPLICATION = 'apps.wsgi.application'

REST_FRAMEWORK = {
    'UNICODE_JSON': False,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardPagination",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dzj_characters',
        'USER': 'dzj',
        'PASSWORD': 'dzjsql',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

AUTH_PROFILE_MODULE = 'account.UserProfile'

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/' # It means home view
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
MEDIA_ROOT = '/data/share/dzj_characters/'
MEDIA_URL = '/'

#DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'
#STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'
COVER_IMAGE_ROOT = MEDIA_ROOT+'cover/'
OPAGE_IMAGE_ROOT = MEDIA_ROOT+'opage_images/'
PAGE_IMAGE_ROOT = MEDIA_ROOT+'page_images/'
CHARACTER_IMAGE_ROOT = MEDIA_ROOT+'character_images/'
CUT_CHARACTER_IMAGE_ROOT = MEDIA_ROOT+'cut_character_images/'

STATIC_ROOT = "/site_media/static"
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

QINIU_ACCESS_KEY= ''
QINIU_SECRET_KEY= ''
QINIU_BUCKET_DOMAIN= ''
QINIU_BUCKET_NAME= ''

QINIU_SECURE_URL = False

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'char_log': {
         'format':'char: %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filters': ['require_debug_true'],
            'filename': 'logs/web_log.log',
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'production_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_production.log',
            'maxBytes': 1024*1024*200, # 200 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'char_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/char_file.log',
            'formatter':'char_log',
        },
    },
    'root': {
        'handlers': ['console', 'default', 'production_logfile'],
        'level': 'DEBUG'
    },
    'loggers': {
        'char_log': {
          'handlers': ['char_file'],
          'level': 'INFO',
          'propagate': False,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

COMPRESS_CSS_FILTERS=['compressor.filters.cssmin.CSSCompressorFilter']
COMPRESS_DATA_URI_MAX_SIZE='1024'

SLACK_TOKEN=''
SLACK_USERNAME=''
SLACK_CHANNEL='#bugs-here'
SLACK_BACKEND='django_slack.backends.UrllibBackend'
