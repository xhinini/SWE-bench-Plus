from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Article
from django.contrib import admin as django_admin
site = admin.AdminSite(name='test_adminsite')
site.register(User)
site.register(Article)
urlpatterns = []