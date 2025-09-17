import sys
import os
import tempfile
import shutil
import importlib
from types import ModuleType, SimpleNamespace
from django.test import TestCase, override_settings
from django.apps import apps
from django.db.migrations.loader import MigrationLoader