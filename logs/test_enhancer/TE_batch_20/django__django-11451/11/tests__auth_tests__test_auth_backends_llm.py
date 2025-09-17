from django.http import HttpRequest
from django.test import TestCase, override_settings
from django.contrib.auth import authenticate, get_user_model
from unittest import mock