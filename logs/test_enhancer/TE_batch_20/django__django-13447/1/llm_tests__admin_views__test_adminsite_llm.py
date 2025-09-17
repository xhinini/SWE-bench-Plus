from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings
from django.urls import path, reverse
from .models import Article
site = admin.AdminSite(name='extra_adminsite')
site.register(User)
site.register(Article)
urlpatterns = [path('extra_admin/admin/', site.urls)]