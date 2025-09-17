from django import forms
from django.test import SimpleTestCase, TestCase
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserChangeForm
from django.contrib.auth.models import User