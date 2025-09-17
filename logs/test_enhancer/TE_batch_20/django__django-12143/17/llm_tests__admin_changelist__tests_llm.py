from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.contrib import admin
from .models import Swallow
from .admin import SwallowAdmin, site as custom_site