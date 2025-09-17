from django.test import TestCase
from django.test.client import RequestFactory
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow