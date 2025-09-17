from django.contrib.auth.backends import RemoteUserBackend
from django.test import override_settings, TestCase
from django.contrib.auth import authenticate, signals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth.models import User