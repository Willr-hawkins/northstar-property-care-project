"""
Base settings for the Northstar Property Care project.

Shared across all environments. Environment-specific settings
live in dev.py and prod.py, which import everything from here.
"""

from pathlib import Path

from decouple import config

# Project root: base.py -> settings/ -> northstar/ -> project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# --------------------------------------------------------------------------
# Security
# --------------------------------------------------------------------------

SECRET_KEY = config("SECRET_KEY")


# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = []

LOCAL_APPS = [
    "core",
    "services",
    "projects",
    "enquiries",
    "dashboard",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# --------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------------------------------
# URLs / WSGI
# --------------------------------------------------------------------------

ROOT_URLCONF = "northstar.urls"

WSGI_APPLICATION = "northstar.wsgi.application"


# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# --------------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"


# --------------------------------------------------------------------------
# Internationalisation
# --------------------------------------------------------------------------

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------
# Static & media files
# --------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------------------------------
# Email
# --------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@northstar.local")
ENQUIRY_NOTIFICATION_EMAIL = config(
    "ENQUIRY_NOTIFICATION_EMAIL", default="enquiries@northstar.local"
)


# --------------------------------------------------------------------------
# Defaults
# --------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"