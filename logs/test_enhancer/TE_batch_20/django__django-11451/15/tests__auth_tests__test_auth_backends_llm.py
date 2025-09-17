from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test import modify_settings
PASSWORD_HASHER_PATH = 'auth_tests.test_auth_backends_regressions.CountingMD5PasswordHasher'