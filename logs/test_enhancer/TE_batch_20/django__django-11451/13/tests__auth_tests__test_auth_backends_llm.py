from django.http import HttpRequest
from django.contrib.auth import authenticate, get_user_model
from django.test import override_settings, TestCase
from .models import CustomUser
from auth_tests.test_auth_backends import CountingMD5PasswordHasher, User