"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os  # Added
from environ import environ  # Added for environ



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

######################## ENVIRON #######################################
env = environ.Env(DEBUG=(bool, False),  # Added. Not necessarily, but recommended to set by default
                  POSTGRES=(bool, True),
                  )

env.read_env(os.path.join(BASE_DIR, ".env"))  # Added for environ. Try to use object, except Class
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [env("ALLOWED_HOST_1"), env("ALLOWED_HOST_2")]


# Application definition

INSTALLED_APPS = [
    ##### native django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ##### 3-rd parties apps


    ##### local apps #####
    "apps.api.client.apps.ClientConfig",
    "apps.api.coach.apps.CoachConfig",
    "apps.api.coach_speciality.apps.CoachSpecialityConfig",
    "apps.api.company.apps.CompanyConfig",
    "apps.api.dynamics.apps.DynamicsConfig",
    "apps.api.group.apps.GroupConfig",
    "apps.api.jwt_auth.apps.JwtAuthConfig",
    "apps.api.mood_category.apps.MoodCategoryConfig",
    "apps.api.status_level.apps.StatusLevelConfig",
    "apps.api.user.apps.UserConfig",
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if env("POSTGRES"):  # Added
    DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql",
                             "NAME": env("DB_NAME_POS"),
                             "USER": env("DB_USER_POS"),
                             "PASSWORD": env("DB_PASSWORD_POS"),
                             "HOST": env("DB_HOST_POS"),
                             "PORT": env("DB_PORT_POS"),
                             }
                 }
else:  # Added
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                             "NAME": BASE_DIR / "db.sqlite3",
                             }
                 }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Poland' - for the Poland for example, not UTC+1

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
