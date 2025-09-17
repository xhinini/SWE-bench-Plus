from unittest.mock import patch
import types
from django.urls import NoReverseMatch
from unittest.mock import patch
import types
from django.urls import NoReverseMatch, reverse
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from .models import Article
from django.contrib import admin
from .test_adminsite import site