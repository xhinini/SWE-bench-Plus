from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import RequestFactory
import re
import urllib.parse
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase