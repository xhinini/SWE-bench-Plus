from django.test import override_settings, TestCase
from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
UserModel = get_user_model()
AUTH_BACKEND = ['django.contrib.auth.backends.ModelBackend']