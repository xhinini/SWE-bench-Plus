import importlib
import django.utils.translation as _ut
import importlib
import django.utils.translation as _ut
from django.test import SimpleTestCase
from django.core.checks import Error
from django.conf import settings as _settings_module
from django.test import override_settings
MOD_NAME = 'django.core.checks.translation'