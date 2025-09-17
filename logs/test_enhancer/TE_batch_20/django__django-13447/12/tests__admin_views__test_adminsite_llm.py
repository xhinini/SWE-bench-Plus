from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase, override_settings
from django.test.client import RequestFactory
from django.urls import path
from django.http import Http404
import types
from .models import Article
site = admin.AdminSite(name='test_adminsite_reg')
site.register(User)
site.register(Article)
urlpatterns = [path('test_admin_reg/admin/', site.urls)]