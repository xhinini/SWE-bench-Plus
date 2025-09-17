from unittest import mock
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.test import TestCase, override_settings
from .models import CustomUser