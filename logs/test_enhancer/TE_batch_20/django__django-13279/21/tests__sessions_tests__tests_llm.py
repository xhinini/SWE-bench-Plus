from django.test import TestCase, override_settings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.conf import settings