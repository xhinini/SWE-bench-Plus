from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import PickleSerializer
import base64

class LegacySha1EncodingTests(SimpleTestCase):

    def setUp(self):
        self.session = CookieSession()