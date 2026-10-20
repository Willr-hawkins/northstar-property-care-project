"""
Development setttings - local machine only.
"""

from decouple import config

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# --------------------------------------------------------------------------
# Database — local PostgreSQL
# --------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# --------------------------------------------------------------------------
# Email — print to the terminal instead of sending
# --------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"