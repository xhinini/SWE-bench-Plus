from django.contrib import admin
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Article
from django.contrib.auth.models import User
site = admin.AdminSite(name='test_adminsite')
try:
    site.register(User)
except Exception:
    pass
try:
    site.register(Article)
except Exception:
    pass