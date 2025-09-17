import re
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, override_settings
from .test_forms import TestDataMixin