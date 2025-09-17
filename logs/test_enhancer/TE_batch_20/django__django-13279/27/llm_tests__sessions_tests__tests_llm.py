from django.test import SimpleTestCase
from django.contrib.sessions.backends.signed_cookies import SessionStore as CookieSession
from django.utils import timezone
from datetime import datetime, timedelta