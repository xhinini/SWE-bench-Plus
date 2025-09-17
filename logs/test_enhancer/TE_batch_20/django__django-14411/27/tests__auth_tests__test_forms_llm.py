from unittest import mock
import re
from django.test import SimpleTestCase
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField