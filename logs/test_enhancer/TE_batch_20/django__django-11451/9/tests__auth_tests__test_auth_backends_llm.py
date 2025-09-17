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