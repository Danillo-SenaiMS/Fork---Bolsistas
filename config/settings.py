import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)

# Lê .env na raiz do projeto. Variáveis sensíveis podem vir via Docker Secrets
# usando _FILE (ex.: SECRET_KEY_FILE=/run/secrets/secret_key).
env.read_env(str(BASE_DIR / '.env'))


def read_secret(name):
    """Retorna valor de segredo: _FILE (Docker Secret) tem prioridade sobre env."""
    file_key = f'{name}_FILE'
    file_path = env(file_key, default=None)
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return env(name, default=None)


SECRET_KEY = read_secret('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('SECRET_KEY deve estar definido no .env ou via Docker Secret.')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', 'bolsas.localhost'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps do projeto
    'base',
    'accounts',
    'cadastro',
    'editais',
    'classificacao',
    'notifications',
    'painel_bolsistas',

    # celery
    'django_celery_beat',
    'dj_celery_panel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processors.perfil_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': env('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
    }
}

# PostgreSQL: sobescreve quando as variáveis de conexão existem.
if env('DB_HOST', default=None):
    DATABASES['default'].update({
        'USER': env('DB_USER'),
        'PASSWORD': read_secret('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', default='5432'),
    })

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Campo_Grande'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cache e result backend do Celery (Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('CACHE_URL', default='redis://redis:6379/1'),
    }
}

# Celery
CELERY_BROKER_URL = env(
    'CELERY_BROKER_URL',
    default='amqp://guest:guest@rabbitmq:5672//',
)
CELERY_RESULT_BACKEND = env(
    'CELERY_RESULT_BACKEND',
    default='redis://redis:6379/0',
)
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 600  # 10 minutos
CELERY_RESULT_EXTENDED = True

# Config futura para S3 (descomentar quando migrar para producao)
# INSTALLED_APPS += ['storages']
# AWS_ACCESS_KEY_ID = read_secret('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = read_secret('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = 'private'
# STORAGES = {
#     'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
#     'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
# }

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguranca em producao
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
    SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simples': {
            'format': '[{levelname}] {asctime} {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simples',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'painel_bolsistas': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'editais': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Integracao com IA (OpenAI)
OPENAI_API_KEY = read_secret('OPENAI_API_KEY')
OPENAI_MODEL = env('OPENAI_MODEL', default='gpt-5.5-mini')
OPENAI_BASE_URL = env('OPENAI_BASE_URL', default='')
