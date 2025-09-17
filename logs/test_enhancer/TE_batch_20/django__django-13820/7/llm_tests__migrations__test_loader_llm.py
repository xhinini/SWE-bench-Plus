from django.db import connection
import sys
import types
from importlib import import_module
from django.test import override_settings
from django.db.migrations.loader import MigrationLoader
from .test_base import MigrationTestBase