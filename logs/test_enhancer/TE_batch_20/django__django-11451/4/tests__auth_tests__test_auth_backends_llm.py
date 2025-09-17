from django.test import override_settings, TestCase
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import MD5PasswordHasher
from django.contrib.auth import get_user_model
from .models import CustomUser
try:
    CountingMD5PasswordHasher
except NameError:

    class CountingMD5PasswordHasher(MD5PasswordHasher):
        calls = 0

        def encode(self, *args, **kwargs):
            type(self).calls += 1
            return super().encode(*args, **kwargs)