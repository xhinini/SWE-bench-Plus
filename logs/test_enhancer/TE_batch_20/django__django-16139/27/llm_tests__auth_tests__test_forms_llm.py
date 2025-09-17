from unittest import mock
import re
import urllib.parse
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User