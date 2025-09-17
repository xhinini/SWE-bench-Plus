import re
import urllib.parse
from django.test import RequestFactory, override_settings, TestCase
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse
import urllib.parse
import re
User = get_user_model()