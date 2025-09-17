from django.test import SimpleTestCase, TestCase, override_settings
import base64
import logging
from django.conf import settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.serializers import PickleSerializer
from django.contrib.sessions.exceptions import SuspiciousSession