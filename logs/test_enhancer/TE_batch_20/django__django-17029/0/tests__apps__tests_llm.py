from django.apps import apps, AppConfig
from django.contrib.admin.models import LogEntry
from django.test import SimpleTestCase, override_settings, isolate_apps
from django.db import models