import base64
import os
import base64
import os
from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession