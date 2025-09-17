from django.utils import timezone
import base64
from django.test import SimpleTestCase, override_settings
from django.contrib.sessions.backends.file import SessionStore as FileSession
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import JSONSerializer, PickleSerializer