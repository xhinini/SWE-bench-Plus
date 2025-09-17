from django.contrib.auth.hashers import MD5PasswordHasher
from unittest import mock
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import MD5PasswordHasher
from django.test import TestCase, override_settings