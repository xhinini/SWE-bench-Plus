from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.test import RequestFactory, override_settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.test import RequestFactory, override_settings
from django.urls import reverse
import urllib.parse
import re
from django.test import TestCase
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .test_forms import TestDataMixin