from unittest import mock
from django.test import TestCase, override_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from .models import CustomUser
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from unittest import mock
from django.test import TestCase, override_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from .models import CustomUser
from auth_tests.test_auth_backends import CountingMD5PasswordHasher