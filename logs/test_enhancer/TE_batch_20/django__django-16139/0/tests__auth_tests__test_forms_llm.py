import re
import urllib.parse
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import RequestFactory, override_settings