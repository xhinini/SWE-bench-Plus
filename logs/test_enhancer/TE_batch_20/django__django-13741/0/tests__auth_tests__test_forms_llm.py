from django.test import SimpleTestCase, TestCase
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX