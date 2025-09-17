from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import override_settings
import re
import urllib.parse
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm
from .test_forms import TestDataMixin