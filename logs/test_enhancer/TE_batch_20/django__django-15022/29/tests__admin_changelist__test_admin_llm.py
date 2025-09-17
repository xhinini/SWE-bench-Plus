from django.test import RequestFactory
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin import site as default_site
from django.contrib.auth.models import User
from .admin import site as test_site
from .models import Parent, Child, Band, Swallow
RequestFactory = RequestFactory()