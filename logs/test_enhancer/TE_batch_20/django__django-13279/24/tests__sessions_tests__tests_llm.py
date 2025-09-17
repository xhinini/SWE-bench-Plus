from django.test import SimpleTestCase, TestCase, override_settings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.backends.cached_db import SessionStore as CacheDBSession
from django.contrib.sessions.backends.file import SessionStore as FileSession
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from .models import SessionStore as CustomDatabaseSession