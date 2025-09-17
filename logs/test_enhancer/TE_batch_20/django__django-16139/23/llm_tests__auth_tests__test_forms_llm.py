from django.test import override_settings, RequestFactory
from django.urls import reverse
import re
import urllib.parse
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.test import TestCase
from .test_forms import TestDataMixin
from django.contrib.auth.models import User