import base64
import pickle
from django.utils.module_loading import import_string
from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession