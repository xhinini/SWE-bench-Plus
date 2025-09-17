from unittest import mock
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from django.test import TestCase, override_settings
UserModel = get_user_model()