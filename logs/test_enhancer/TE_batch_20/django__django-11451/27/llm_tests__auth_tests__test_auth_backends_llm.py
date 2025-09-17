from django.test import TestCase, override_settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import User
from django.db import connection
UserModel = get_user_model()