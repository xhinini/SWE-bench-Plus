from django.apps import AppConfig, apps
from django.apps.registry import Apps
from django.test import SimpleTestCase, override_settings, isolate_apps
from django.test.utils import extend_sys_path
from django.core.exceptions import AppRegistryNotReady, ImproperlyConfigured
SOME_INSTALLED_APPS = ['apps.apps.MyAdmin', 'apps.apps.MyAuth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles']