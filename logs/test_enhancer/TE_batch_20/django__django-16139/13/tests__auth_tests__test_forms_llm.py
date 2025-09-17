from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.test import RequestFactory
import re
import urllib.parse
from django.test import override_settings
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BuiltinUserAdmin
from django.contrib.admin import AdminSite as BuiltinAdminSite
from django.test import RequestFactory as DjangoRequestFactory