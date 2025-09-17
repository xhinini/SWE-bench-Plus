from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
import re
import urllib.parse
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
import re
import urllib.parse