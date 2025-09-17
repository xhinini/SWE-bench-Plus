from django.test import override_settings, TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow