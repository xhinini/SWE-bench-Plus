from django.test import TestCase, override_settings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import JSONSerializer, PickleSerializer
from django.test import TestCase, override_settings
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.contrib.sessions.serializers import JSONSerializer, PickleSerializer