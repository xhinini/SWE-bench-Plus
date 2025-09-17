from django import forms
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from unittest import mock
from django import forms
from django.test import SimpleTestCase
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX