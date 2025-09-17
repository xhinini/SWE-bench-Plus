from django.contrib.auth.forms import ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, override_settings
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
import re