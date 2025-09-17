from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow