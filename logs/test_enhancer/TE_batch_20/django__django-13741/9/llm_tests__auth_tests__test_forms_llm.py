from django.test import SimpleTestCase, TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError