import sys
import types
import pkgutil
from importlib import import_module, reload
from unittest.mock import patch
from django.apps import apps
from importlib import reload as importlib_reload
from unittest.mock import patch
import sys
import types
from django.test import TestCase, override_settings
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.exceptions import BadMigrationError