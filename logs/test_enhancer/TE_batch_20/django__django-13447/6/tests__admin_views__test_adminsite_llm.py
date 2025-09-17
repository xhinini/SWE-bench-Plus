from unittest.mock import patch
from django.test.client import RequestFactory
from django.urls import reverse
from django.http import Http404
from unittest.mock import patch
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, SimpleTestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.http import Http404
from admin_views.test_adminsite import site as test_site, Article, User