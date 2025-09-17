from django.apps import apps
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import SimpleTestCase, override_settings
from django.test.utils import isolate_apps