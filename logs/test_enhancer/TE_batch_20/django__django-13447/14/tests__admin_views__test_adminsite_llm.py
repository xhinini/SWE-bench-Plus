from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article
from django.contrib import admin
from admin_views.test_adminsite import site