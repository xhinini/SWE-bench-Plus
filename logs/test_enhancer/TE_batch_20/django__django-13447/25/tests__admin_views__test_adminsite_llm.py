from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.http import Http404
from .test_adminsite import site as test_site
from .models import Article