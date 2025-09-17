from django.contrib.admin import ModelAdmin
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Article
from django.contrib.auth.models import User
from .test_adminsite import site