from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings, SimpleTestCase
from django.urls import reverse
from django.http import Http404
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from .test_adminsite import site, Article
from django.test import SimpleTestCase