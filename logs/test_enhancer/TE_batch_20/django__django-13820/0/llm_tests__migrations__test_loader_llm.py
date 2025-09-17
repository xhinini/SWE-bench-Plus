import types
from importlib import import_module as real_import_module
import django.db.migrations.loader as loader_mod
import types
from importlib import import_module as real_import_module
import pkgutil
from django.db import connection
from django.db.migrations.loader import MigrationLoader
import django.db.migrations.loader as loader_mod
from django.test import TestCase, override_settings, modify_settings

def _use_fake_top_module(top_module_name, fake_module):
    """
    Context-manager-like helper to monkeypatch loader_mod.import_module so
    that only imports of the top_module_name return fake_module, and all
    other imports use the real import_module. Returns a restoration function.
    """
    orig_import = loader_mod.import_module

    def _patched_import(name, *args, **kwargs):
        if name == top_module_name:
            return fake_module
        return real_import_module(name, *args, **kwargs)
    loader_mod.import_module = _patched_import

    def _restore():
        loader_mod.import_module = orig_import
    return _restore