from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sessions.serializers import JSONSerializer, PickleSerializer
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.test import SimpleTestCase, override_settings