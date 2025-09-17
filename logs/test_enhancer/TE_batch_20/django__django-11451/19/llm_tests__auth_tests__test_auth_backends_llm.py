from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.test import TestCase
UserModel = get_user_model()

class ModelBackendAuthenticateGuardTests(TestCase):

    def setUp(self):
        self.backend = ModelBackend()

from unittest import mock
from django.test import TestCase, override_settings
import django.contrib.auth.backends as backends
from django.contrib.auth.backends import ModelBackend

class ModelBackendAuthenticateRegressionTests(TestCase):

    def setUp(self):
        self.backend = ModelBackend()
        self.UserModel = backends.UserModel

from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings
from django.http import HttpRequest
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings
from django.http import HttpRequest
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
USERNAME_FIELD = get_user_model().USERNAME_FIELD

@override_settings(PASSWORD_HASHERS=['auth_tests.test_auth_backends.CountingMD5PasswordHasher'])
class AuthenticateMissingCredentialsTests(TestCase):
    """
    Ensure that authenticate() performs no DB queries and does not run
    password hashers when username or password is missing (None).
    """

    def setUp(self):
        CountingMD5PasswordHasher.calls = 0