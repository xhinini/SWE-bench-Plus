from django.utils import timezone
from django.test import SimpleTestCase, override_settings
import base64
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession