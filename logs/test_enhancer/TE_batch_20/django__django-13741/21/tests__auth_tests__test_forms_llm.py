from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.forms import AdminPasswordChangeForm, ReadOnlyPasswordHashField, UserChangeForm, ReadOnlyPasswordHashWidget
from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.core.exceptions import ValidationError