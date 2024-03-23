"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
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
    "debug_toolbar",  # Added
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ##### 3-rd parties apps
    "rest_framework",  # Added for DjangoRestFramework
    "rest_framework_simplejwt",
    "django_resized",
    "admin_reorder",  # To reorder admin panel side bar
    "drf_yasg",  # Added for SWAGER
    "PIL",

    ##### local apps #####
    "apps.api.utils.apps.UtilsConfig",
    "apps.api.messages_api.apps.MessagesApiConfig",
    "apps.api.client_status.apps.ClientStatusConfig",
    "apps.api.coach.apps.CoachConfig",
    "apps.api.coach_speciality.apps.CoachSpecialityConfig",
    "apps.api.company.apps.CompanyConfig",
    "apps.api.dynamics.apps.DynamicsConfig",
    "apps.api.training_group.apps.TrainingGroupConfig",
    "apps.api.jwt_auth.apps.JwtAuthConfig",
    "apps.api.emotional_level.apps.MoodLevelConfig",
    "apps.api.status_level.apps.StatusLevelConfig",
    "apps.api.user.apps.UserConfig",
    "apps.api.gender.apps.GenderConfig",
    "apps.api.country.apps.CountryConfig",
    "apps.api.department.apps.DepartmentConfig",
    "apps.api.training_year.apps.TrainingYearConfig",
    "apps.api.self_satisfaction_level.apps.SelfSatisfactionLevelConfig",
    "apps.api.administrator.apps.AdministratorConfig",
    "apps.api.client.apps.ClientConfig",
    "apps.api.group_client_payment.apps.GroupClientPaymentConfig",
    "apps.api.group_client_start_data.apps.GroupClientStartDataConfig",
    "apps.api.group_client_progress.apps.GroupClientProgressDataConfig",
    "apps.api.payment_type.apps.PaymentTypeConfig",
    "apps.api.payment_document.apps.PaymentDocumentConfig",
    "apps.api.group_many_client.apps.GroupManyClientConfig",
    "apps.api.group_many_administrator.apps.GroupManyAdministratorConfig",
    "apps.api.group_many_coach.apps.GroupManyCoachConfig",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Added

    # "admin_reorder.middleware.ModelAdminReorder",  # To reorder admin panel side bar

]


ROOT_URLCONF = 'config.urls'
AUTH_USER_MODEL = "user.User"  # IMPORTANT: NECESSARY FOR CUSTOM USER

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates',],
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


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication'
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework.permissions.AllowAny",  # if not defined any permission, will be AllowAny by default
        # "rest_framework.permissions.IsAuthenticated",  # DM added: For standard Django permissions work good
        # "rest_framework.permissions.IsAdminUser",  # DM added: For standard Django permissions work good
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "apps.jwt_config.serializers.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Poland' - for the Poland for example, not UTC+1

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



######################## COLLECTING STATIC #############################
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "apps", "api", "<apps_name_1>", "static"),  # additional dirs with static files
#     os.path.join(BASE_DIR, "apps", "api", "<apps_name_2>", "static"),  # if necessary
# ]

STATIC_URL = "static/"  # =<each_app_dir>/static - apps dirs, where finder will find static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # =<root_proj_dir>/static - where all collected static files will be collected

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


################## AUTHENTICATION BY USERNAME|EMAIL ####################
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Standard AUTH.MODELS django auth by username, if not -> next Backend
    "apps.api.user.authentications.CustomAuthByEmailBackend",  # Custom auth by email
    "apps.api.user.authentications.CustomAuthByNickNameBackend",  # Custom auth by nickname
]


# ADMIN_REORDER = (
#     ("user", ("User", )),
#     ("administrator", ("Administrator", ))
# )
