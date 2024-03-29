from pathlib import Path
import os
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

ENV = config('ENVIRONMENT')
SECRET_KEY = config('SECRET_KEY')
BASE_DIR = Path(__file__).resolve().parent.parent

if 'production' in ENV:

    DEBUG = False
    ALLOWED_HOSTS = ['*']


    sentry_sdk.init(
        dsn="https://ce5d2c2138fc4cd4b8d1c04c5fa91982@o936455.ingest.sentry.io/5886823",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

else:

    DEBUG = True

    ALLOWED_HOSTS = ['*', 'http://164.90.198.149/',
                     '127.0.0.1',
                     'cryptotradebot.io',
                     'www.cryptotradebot.io',
                     'https://www.cryptotradebot.io/',
                     'www.app.funer24.com',
                     'dashboard.cryptotradebot.io'
                     ]


CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(config('REDIS_HOST'), 6379)],
            },
        },
    }



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'analytics',
    'bot',
    'backtest',
    'exchange',
    'strategy',
    'csvexport',
    'dbbackup',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'django_quill',
    'channels',
]

QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    {'header': [1, 2, False]},
                    {'align': []},
                    'code-block',
                    {'color': []},
                    {'background': []},
                ],
                ['code-block', ],
                ['clean'],
            ]
        }
    }
}

DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_DEFAULT_ACL = None
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': config('DBBACKUP_STORAGE_OPTIONS_ACCESS_KEY'),
    'secret_key': config('DBBACKUP_STORAGE_OPTIONS_SECRET_KEY'),
    'bucket_name': 'tastradingsystem'
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['sentry'],
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#     },
#     'handlers': {
#         'sentry': {
#             'level': 'DEBUG',
#             'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'ERROR',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'raven': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'sentry.errors': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#     },
# }

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

# WSGI_APPLICATION = 'tas.wsgi.application'
ASGI_APPLICATION = 'tas.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DJANGO_POSTGRES_HOST'),
        'PORT': config('DJANGO_POSTGRES_PORT'),
    }
}

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

LANGUAGE_CODE = 'it-IT'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_L10N = True
AUTH_USER_MODEL = 'exchange.User'
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "tas/static")]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
