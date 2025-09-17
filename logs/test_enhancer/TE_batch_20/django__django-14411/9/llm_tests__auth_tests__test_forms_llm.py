from django import forms
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User