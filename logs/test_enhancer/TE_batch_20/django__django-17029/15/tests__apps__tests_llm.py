from django.apps import apps
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.test import SimpleTestCase, override_settings
from django.db import models