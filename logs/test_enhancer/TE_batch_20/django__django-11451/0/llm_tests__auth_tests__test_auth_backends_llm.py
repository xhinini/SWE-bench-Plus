from unittest import mock
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings
from .test_auth_backends import CountingMD5PasswordHasher
from unittest import mock
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings
from .test_auth_backends import CountingMD5PasswordHasher
UserModel = get_user_model()