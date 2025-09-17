from django.apps import apps
from django.contrib import admin
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article
from django.apps import apps
site = admin.AdminSite(name='test_adminsite')
site.register(User)
site.register(Article)