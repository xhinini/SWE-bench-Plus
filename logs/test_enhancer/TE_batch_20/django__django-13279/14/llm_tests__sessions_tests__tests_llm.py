import base64
from django.test import SimpleTestCase, override_settings
from django.conf import settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import PickleSerializer