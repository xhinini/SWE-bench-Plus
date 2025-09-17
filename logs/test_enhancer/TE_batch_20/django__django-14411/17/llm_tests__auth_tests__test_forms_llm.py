from django import forms
from django.forms import fields
from django.test import SimpleTestCase, TestCase
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.contrib.auth.models import User