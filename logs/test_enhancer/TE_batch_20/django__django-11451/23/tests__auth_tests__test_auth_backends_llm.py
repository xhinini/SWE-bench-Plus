from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, override_settings
from .models import CustomUser, UUIDUser
from django.contrib.auth.models import User
from .test_auth_backends import CountingMD5PasswordHasher