from pathlib import Path
import os, logging

BASE_DIR = Path(__file__).resolve().parent.parent

# Fetches the environment variable, defaulting to 'production' if not found
DJANGO_ENV = os.environ.get("DJANGO_ENV", "production").lower()
# Sets DEBUG to True only if the environment is strictly 'development'
DEBUG = DJANGO_ENV == "development"

# SECURITY WARNING: keep the secret key used in production!
SECRET_KEY = 'django-insecure-#fs5^#gsc+tuvh+pty=$p^0wq+*ip3*o0ojno&$a&l^pbfoeh%'

# Allow any IP for development and image distribution — fine for local use
# For production, you should specify the allowed hosts explicitly i.e. the hostname or IP address of your server where easySIPp is deployed.
ALLOWED_HOSTS = ['*']

# CSRF settings — safe default for local-only access
CSRF_TRUSTED_ORIGINS = []  # Empty is fine for HTTP usage only

# Only needed if you use HTTPS behind a proxy (not needed now)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'easySIPp',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = None

ROOT_URLCONF = 'easySIPp_project.urls'

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
                'easySIPp.context_processors.version_context'
            ],
        },
    },
]

# WSGI_APPLICATION = 'easySIPp_project.wsgi.application'
ASGI_APPLICATION = 'easySIPp_project.asgi.application'

# Localization
LANGUAGE_CODE = 'en-us'

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'collectstatic/'

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Logging
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

class RenameUvicornFilter(logging.Filter):
    def filter(self, record):
        record.name = 'uvicorn'  # Overrides 'uvicorn.error' log prints e.g. "uvicorn.error: Started server process" which is misleading
        return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'rename_uvicorn': {
            '()': RenameUvicornFilter,
        }
    },
    'formatters': {
        'default': {
            'format': '{asctime} {levelname:<8} {name} →  {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'verbose': {
            'format': '{asctime} {levelname:<8} {name} -- {filename}:{lineno} →  {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'handlers': {
        # Console for warnings and above only
        'console_warn': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'default',
        },
        # Console for everything
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'server_file': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': LOG_DIR / 'server.log',
            'formatter': 'default',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        'app_file': {
            'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
            'filename': LOG_DIR / 'easySIPp.log',
            'formatter': 'verbose',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 3,
            'encoding': 'utf-8',
        },
    },
    # Third-party libraries: warnings and above, console only
    'root': {
        'handlers': ['console_warn'],
        'level': 'WARNING',
    },
    'loggers': {
        # Django -> console (WARNING+) and server.log (DEBUG/INFO+)
        'django': {
            'handlers': ['console_warn', 'server_file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.db.backends': {'level': 'WARNING'},  # set to DEBUG to see all SQL
        # uvicorn -> console (WARNING+) and server.log (DEBUG/INFO+)
        'uvicorn': {
            'handlers': ['console_warn', 'server_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.access': {'handlers': [], 'propagate': True},
        # uvicorn.errors to console and server.log
        'uvicorn.error': {'handlers': ['console', 'server_file'], 'filters': ['rename_uvicorn'], 'propagate': False},

        # easySIPp -> console (everything) and app.log
        'easySIPp': { 
            'handlers': ['console', 'app_file'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}