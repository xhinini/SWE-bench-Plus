from django.test import SimpleTestCase, override_settings
from django.core import signing
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import PickleSerializer
import base64
import logging