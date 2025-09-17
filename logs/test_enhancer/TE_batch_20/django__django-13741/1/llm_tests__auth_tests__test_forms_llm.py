from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from .test_forms import TestDataMixin
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError