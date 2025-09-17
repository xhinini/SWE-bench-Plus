from django.contrib.auth import authenticate
from django.test import TestCase, override_settings
from .test_auth_backends import CountingMD5PasswordHasher