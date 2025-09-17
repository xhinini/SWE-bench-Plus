from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.serializers import PickleSerializer
import base64