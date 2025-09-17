from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
UserModel = get_user_model()