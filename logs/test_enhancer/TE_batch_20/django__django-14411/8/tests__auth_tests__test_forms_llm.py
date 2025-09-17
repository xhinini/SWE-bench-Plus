from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.test import override_settings
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.test import override_settings
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget, ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.test import TestCase