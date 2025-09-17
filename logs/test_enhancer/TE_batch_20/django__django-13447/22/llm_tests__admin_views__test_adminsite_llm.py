from admin_views.test_adminsite import site as module_site, Article, User
from django.contrib import admin
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.http import Http404
from admin_views.test_adminsite import site as module_site, Article, User