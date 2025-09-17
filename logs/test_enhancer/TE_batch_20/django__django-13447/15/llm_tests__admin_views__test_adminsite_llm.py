from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from .models import Article
from .test_adminsite import site as test_site