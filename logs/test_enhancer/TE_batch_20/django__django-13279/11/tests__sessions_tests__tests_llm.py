from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import PickleSerializer
import base64

class LegacySha1EncodingTests(SimpleTestCase):

    def setUp(self):
        self.session = CookieSession()

from django.conf import settings
from django.test import TestCase, override_settings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.serializers import PickleSerializer
import base64

class LegacyEncodeTests(TestCase):

    def tearDown(self):
        try:
            self.session.delete()
        except Exception:
            pass
new_imports_code: ''

from django.utils import timezone
from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import JSONSerializer, PickleSerializer
import base64
import string

class LegacyEncodingRegressionTests(SimpleTestCase):

    def setUp(self):
        self.session = CookieSession()