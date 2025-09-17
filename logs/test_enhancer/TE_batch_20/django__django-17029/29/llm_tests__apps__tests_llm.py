import threading
from django.apps import apps
from django.test import SimpleTestCase, override_settings, isolate_apps
from django.contrib.admin.models import LogEntry
import threading
from .models import TotallyNormal