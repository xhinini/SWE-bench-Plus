from django.apps import AppConfig, apps
from django.apps.registry import Apps
from django.test import SimpleTestCase, override_settings
from django.test.utils import isolate_apps
from types import SimpleNamespace
new_imports_code: ''