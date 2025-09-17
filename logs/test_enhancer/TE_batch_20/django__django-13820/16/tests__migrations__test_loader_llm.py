import types
from importlib import import_module
from django.test import override_settings, TestCase
from django.db.migrations.loader import MigrationLoader
from django.db import connection