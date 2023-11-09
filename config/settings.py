"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os, sys
from django.contrib.messages import constants as messages
from datetime import timedelta
import environ
import platform

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = (environ.Path(__file__) - 1)
APPS_DIR = ROOT_DIR.path("apps")

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tn0y5u-zdy_=u=7+mp&r@46-rl=bdro+6tmcqupd_nwpa&k6^c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS =  env("ALLOWED_HOSTS", default=['0.0.0.0','localhost','localhost:8000','127.0.0.1','127.0.0.1:8000','127.0.0.1:8001'])

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'treebeard',
    'rangefilter',
    'ajax_select'
]

THIRD_PARTY_APPS = [
    "adminlteui.apps.AdminlteUIConfig",
    'constance',
    'constance.backends.database',
    'mozilla_django_oidc',
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt',
    "reversion",
]

LOCAL_APPS = [
    'apps.core',
    'apps.users',
    'apps.session',
    'apps.django_sso_app',
    'apps.contrib',
    'apps.certidao_localizacao',
    'apps.lembrete'
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',    
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "apps.session.middleware.SessionMiddleware",
]

ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME',default='css') ,
        'USER': env('DB_USER',default='postgres'),
        'PASSWORD': env('DB_PASSWORD',default='postgres'),
        'HOST': env('DB_HOST',default='localhost')
    }
}


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
    10,
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}


TOKEN_LIFETIME_DAY = 1

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_COOKIE_AGE = 24 * 60 * 60

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=TOKEN_LIFETIME_DAY),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

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
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

DOMINIO_ATUAL = env('DOMINIO_ATUAL', default='localhost:8000')
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
   'DOMINIO_ATUAL': (DOMINIO_ATUAL,
                'Dominio atual do sistema',
                str),
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    {
        "NAME": "apps.session.password_validation.UpperCase",
        "OPTIONS": { "min_length": 1 }
    },
    {
        "NAME": "apps.session.password_validation.SpecialCase",
        "OPTIONS": { "min_length": 1 }
    },
    {
        "NAME": "apps.session.password_validation.RepeticaoCase",
        "OPTIONS": { "min_length": 2 }
    },
    {
        "NAME": "apps.session.password_validation.AcentoCase",
    },
    {
        "NAME": "apps.session.password_validation.OldPassword",
        "OPTIONS": { "min_length": 3 }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = ( env('STATIC_URL', default=os.path.join(BASE_DIR, 'staticfiles')), )
STATIC_URL = env('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.join('static')


# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = env('MEDIA_URL', default='/media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Configurações de CORS
CORS_ALLOWED_ORIGINS = env("DJANGO_CORS_ALLOWED_ORIGINS", default=[
    'http://0.0.0.0:8000',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    "https://stage-app.defensoria.ce.def.br",
    "http://192.168.0.121:8000",
    "http://localhost:19006","http://127.0.0.1:3000"])


CORS_ORIGIN_WHITELIST = env("DJANGO_CORS_ORIGIN_WHITELIST", default=[
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    "https://stage-app.defensoria.ce.def.br",
    "http://192.168.0.121:8000",
    "http://localhost:19006","http://127.0.0.1:3000"])


ADMINLTE_SETTINGS = {
    'search_form': False,
    'demo': False,
    'skin': 'green'
}

ENCRYPT_KEY = b'z-eIxGbdQ3QlLoB9stT9QhluFpxXsNoYsgpHN_fGXAg='

if platform == "linux" or platform == "linux2":
    WKHTMLTOPDF_CMD = env("WKHTMLTOPDF_CMD", default='wkhtmltopdf')
elif platform == "win32":
    WKHTMLTOPDF_CMD = 'C:/"Program Files"/wkhtmltopdf/bin/wkhtmltopdf.exe'


WKHTMLTOPDF_CMD_OPTIONS = {
    'quiet': True,
}

LOGIN_URL = '/admin'

#FusionAuth CONFIGS
# The below config values should be taken from FusionAuth application
USE_FUSIONAUTH = env("USE_FUSIONAUTH",default=False)
USER_PASSWORD_TEST = env("USER_PASSWORD_TEST",default='Dpgeceti@20xx')

if USE_FUSIONAUTH:
    FUSIONAUTH_HOST = env("FUSIONAUTH_HOST",default="http://127.0.0.1:9011/")
    OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID",default="")
    OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET",default="")
    
    # Replace localhost with the machine's IP address where the FusionAuth application is running if not on localhost
    OIDC_OP_AUTHORIZATION_ENDPOINT = FUSIONAUTH_HOST + "oauth2/authorize"
    OIDC_OP_TOKEN_ENDPOINT = FUSIONAUTH_HOST + "oauth2/token"
    OIDC_OP_USER_ENDPOINT = FUSIONAUTH_HOST + "oauth2/userinfo"
    OIDC_OP_JWKS_ENDPOINT = FUSIONAUTH_HOST + ".well-known/jwks.json"

    # Replace localhost with the machine's IP address where the Django application is running if not on localhost
    LOGIN_REDIRECT_URL = "/admin"
    LOGOUT_REDIRECT_URL = "/oidc/callback/"

    FUSIONAUTH_USER_API_KEY = env("FUSIONAUTH_USER_API_KEY",default="I0tmvHlM0mNLwNNsVGs_2F9jVK5SQp_hbKUlLKPH-cskQShspmGG2-3z")
    AUTHENTICATION_BACKENDS = (
        'apps.django_sso_app.MyAuthenticationBackend.MyAuthenticationBackend',
    )