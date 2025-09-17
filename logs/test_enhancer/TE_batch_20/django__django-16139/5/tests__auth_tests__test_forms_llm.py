import urllib.parse
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import RequestFactory, override_settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import RequestFactory, override_settings
from django.urls import reverse
import re
from django.test import TestCase
from .test_forms import TestDataMixin
from django.contrib.auth.forms import UserChangeForm