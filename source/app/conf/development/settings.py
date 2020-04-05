import os
import warnings
from django.utils.translation import ugettext_lazy as _
from os.path import dirname
import psycopg2.extensions

warnings.simplefilter("error", DeprecationWarning)

BASE_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))
CONTENT_DIR = os.path.join(BASE_DIR, "content")

SECRET_KEY = "NhfTvayqggTBPswCXXhWaN69HuglgZIkM"

STRIPE_SECRET_KEY = 'sk_test_oHZ6TtwogfqBddcaf8sqG9Np005eQ5e5OA'
STRIPE_PUBLISHABLE_KEY = 'pk_test_FAFu3glBDqdKrdvJNOiF94iZ00LEThelHv'

LICENSE_SECRET='license key secret, change me'  # Used in source/payment/keygen.py

DEBUG = True
ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Vendor apps
    "bootstrap4",
    # Application apps
    "main",
    "accounts",
    'payment',
    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.steam',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(CONTENT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(CONTENT_DIR, "tmp/emails")
EMAIL_HOST_USER = "test@example.com"
DEFAULT_FROM_EMAIL = "test@example.com"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "127.0.0.1",
        "USER": "root",
        "PASSWORD": "toor",
        "NAME": "postgres",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "accounts:log_in"
USE_REMEMBER_ME = True

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

SIGN_UP_FIELDS = [
    "username",
    "first_name",
    "last_name",
    "email",
    "password1",
    "password2",
]

if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ["first_name", "last_name", "email", "password1", "password2"]

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
    ("zh-Hans", _("Simplified Chinese")),
]

TIME_ZONE = "UTC"
USE_TZ = True

STATIC_ROOT = os.path.join(CONTENT_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(CONTENT_DIR, "media")
MEDIA_URL = "/media/"

STATICFILES_DIRS = [os.path.join(CONTENT_DIR, "assets")]

LOCALE_PATHS = [os.path.join(CONTENT_DIR, "locale")]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

