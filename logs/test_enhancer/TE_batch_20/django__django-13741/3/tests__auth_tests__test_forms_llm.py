from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm, AdminPasswordChangeForm, AdminPasswordChangeForm as APForm
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.core.exceptions import ValidationError