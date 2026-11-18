"""
Production settings — Render.

Skeleton for now. Database (DATABASE_URL), WhiteNoise, S3 media,
SendGrid and the remaining security settings are completed in
Sprint 6 (Production settings & security / Render deployment).
"""

from decouple import Csv, config

from .base import *  # noqa: F401,F403

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv(), default="")


# --------------------------------------------------------------------------
# Security
# --------------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# --------------------------------------------------------------------------
# Email — SendGrid SMTP (Django 6.1 MAILERS)
# --------------------------------------------------------------------------

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": "smtp.sendgrid.net",
            "use_tls": True,  # port 587 is the default with TLS
            "username": "apikey",  # SendGrid's SMTP username is literally "apikey"
            "password": config("SENDGRID_API_KEY"),
            "timeout": 10,  # never leave a customer waiting on a slow mail server
        },
    },
}