from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from django.http import HttpRequest
from django.test import TestCase, override_settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from auth_tests.test_auth_backends import CountingMD5PasswordHasher