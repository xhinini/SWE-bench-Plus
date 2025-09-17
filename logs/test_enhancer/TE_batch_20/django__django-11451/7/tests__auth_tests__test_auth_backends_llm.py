from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.test import TestCase
UserModel = get_user_model()

class ModelBackendAuthenticateGuardTests(TestCase):

    def setUp(self):
        self.backend = ModelBackend()