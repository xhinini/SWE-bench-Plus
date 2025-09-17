pass
from unittest import mock
import importlib
from django.test import TestCase, override_settings
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
auth_backends = importlib.import_module('django.contrib.auth.backends')
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from django.contrib.auth.models import User