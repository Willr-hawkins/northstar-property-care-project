"""
Test settings - used only by pytest
"""

from .dev import *

# A fast hasher makes creating test users far quicker; never use it outside tests
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]