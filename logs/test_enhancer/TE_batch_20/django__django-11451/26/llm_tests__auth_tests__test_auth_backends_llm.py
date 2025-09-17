from django.contrib.auth import authenticate
from django.test import TestCase, override_settings
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from .models import CustomUser, UUIDUser, ExtensionUser, CustomPermissionsUser, CustomUserWithoutIsActiveField, User
from django.contrib.auth import authenticate
from django.test import TestCase, override_settings
from auth_tests.test_auth_backends import CountingMD5PasswordHasher
from .models import CustomUser, UUIDUser, ExtensionUser, CustomPermissionsUser, CustomUserWithoutIsActiveField, User