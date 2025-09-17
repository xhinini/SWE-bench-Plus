from django.test import TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from .test_forms import TestDataMixin as BaseTestDataMixin