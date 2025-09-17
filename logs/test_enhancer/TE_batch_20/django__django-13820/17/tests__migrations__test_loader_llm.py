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

import types
import tempfile
import shutil
import pkgutil
from importlib import reload
import sys
import types
import tempfile
import shutil
import pkgutil
from importlib import reload
from django.test import TestCase, override_settings
from django.conf import settings
from django.apps import apps
from django.db.migrations.loader import MigrationLoader

def _install_fake_app_config(monkeyed_list):
    """
    Replace apps.get_app_configs to return a list of MockAppConfig instances.
    Returns a function to restore the original.
    """
    original = apps.get_app_configs
    apps.get_app_configs = lambda: monkeyed_list
    return original

def _restore_app_configs(original):
    apps.get_app_configs = original

def _cleanup_module(module_name, tempdir=None):
    sys.modules.pop(module_name, None)
    sys.modules.pop(f'{module_name}.migrations', None)
    if tempdir:
        try:
            shutil.rmtree(tempdir)
        except Exception:
            pass

from types import ModuleType, SimpleNamespace
import sys
from collections import deque
from unittest.mock import patch
from types import ModuleType, SimpleNamespace
import sys
from collections import deque
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.db.migrations.loader import MigrationLoader

class LoaderNamespacePackageTests(TestCase):
    """
    Test MigrationLoader.load_disk handling of __file__ and __path__ variations.
    """

    def _make_app_config(self, label='fake'):
        return SimpleNamespace(label=label, name='fakepkg')

from types import ModuleType, SimpleNamespace
from unittest.mock import patch
import types
from types import SimpleNamespace, ModuleType
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.db.migrations.loader import MigrationLoader

class LoaderModuleAttributesTests(TestCase):
    """
    Tests for MigrationLoader.load_disk() handling of module __file__ and __path__.
    """

    def setUp(self):

        class SimpleMigration:
            dependencies = []
            run_before = []
            replaces = []
            atomic = True

            def __init__(self, name, app_label):
                self.name = name
                self.app_label = app_label
        self.SimpleMigration = SimpleMigration
        self.app_config = SimpleNamespace(label='fakeapp', name='fakeapp')

from importlib import import_module
from django.test import override_settings
from django.db.migrations.loader import MigrationLoader
from django.db import connection

def _get_migrations_for_module_state(modify_path=None, modify_file=None):
    """
    Helper to import the test migrations module and modify its __path__/__file__
    then run MigrationLoader.load_disk() to inspect behaviour.
    Returns (disk_migration_names, unmigrated_apps, migrated_apps).
    """
    test_module = import_module('migrations.test_migrations')
    orig_path = list(test_module.__path__)
    had_file = hasattr(test_module, '__file__')
    orig_file = getattr(test_module, '__file__', None)
    orig_spec = getattr(test_module, '__spec__', None)
    orig_spec_origin = None
    orig_spec_has_location = None
    if orig_spec is not None:
        orig_spec_origin = getattr(orig_spec, 'origin', None)
        orig_spec_has_location = getattr(orig_spec, 'has_location', None)
    try:
        if modify_path is not None:
            test_module.__path__ = modify_path
        if modify_file == 'del':
            if hasattr(test_module, '__file__'):
                delattr(test_module, '__file__')
            if test_module.__spec__ is not None:
                test_module.__spec__.origin = None
                test_module.__spec__.has_location = False
        elif modify_file == 'keep':
            test_module.__file__ = orig_file
            if test_module.__spec__ is not None:
                test_module.__spec__.origin = orig_spec_origin
                test_module.__spec__.has_location = orig_spec_has_location
        loader = MigrationLoader(connection, load=False)
        loader.load_disk()
        migrations = [name for app, name in loader.disk_migrations if app == 'migrations']
        return (migrations, loader.unmigrated_apps, loader.migrated_apps)
    finally:
        test_module.__path__[:] = orig_path
        if had_file:
            test_module.__file__ = orig_file
        elif hasattr(test_module, '__file__'):
            delattr(test_module, '__file__')
        if orig_spec is not None:
            test_module.__spec__.origin = orig_spec_origin
            test_module.__spec__.has_location = orig_spec_has_location

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_tuple_path_treated_as_namespace(self):
    """A tuple __path__ with no __file__ should be treated as a namespace package (ignored)."""
    test_module = import_module('migrations.test_migrations')
    orig = list(test_module.__path__)
    tuple_path = tuple(orig)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=tuple_path, modify_file='del')
    self.assertEqual(migrations, [])
    self.assertIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_custom_path_obj_treated_as_namespace(self):
    """A custom non-list __path__ object with no __file__ should be treated as a namespace package (ignored)."""

    class CustomPath(object):

        def __init__(self, seq):
            self._seq = list(seq)

        def __iter__(self):
            return iter(self._seq)

        def __len__(self):
            return len(self._seq)
    test_module = import_module('migrations.test_migrations')
    custom = CustomPath(test_module.__path__)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=custom, modify_file='del')
    self.assertEqual(migrations, [])
    self.assertIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_list_subclass_path_treated_as_regular_package(self):
    """A list subclass __path__ with no __file__ should be treated as a regular package (migrations discovered)."""

    class MyList(list):
        pass
    test_module = import_module('migrations.test_migrations')
    subclass_list = MyList(test_module.__path__)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=subclass_list, modify_file='del')
    self.assertCountEqual(migrations, ['0001_initial', '0002_second'])
    self.assertNotIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_list_path_with_no_file_is_accepted(self):
    """A plain list __path__ with no __file__ is a supported frozen-package case (migrations discovered)."""
    test_module = import_module('migrations.test_migrations')
    list_path = list(test_module.__path__)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=list_path, modify_file='del')
    self.assertCountEqual(migrations, ['0001_initial', '0002_second'])
    self.assertNotIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_file_present_but_path_tuple_loads_migrations(self):
    """If __file__ is present (not a frozen env) but __path__ is tuple, treat as package and load migrations."""
    test_module = import_module('migrations.test_migrations')
    orig_path = list(test_module.__path__)
    tuple_path = tuple(orig_path)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=tuple_path, modify_file='keep')
    self.assertGreaterEqual(len(migrations), 1)
    self.assertNotIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_removing_path_attribute_results_in_unmigrated(self):
    """If the module has no __path__ attribute (single-file module), it is treated as unmigrated."""
    test_module = import_module('migrations.test_migrations')

    class ProxyModule:
        pass
    orig_path = list(test_module.__path__)
    try:
        delattr(test_module, '__path__')
        loader = MigrationLoader(connection, load=False)
        loader.load_disk()
        self.assertIn('migrations', loader.unmigrated_apps)
    finally:
        test_module.__path__[:] = orig_path

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_namespace_with_has_location_false_and_no_file(self):
    """Explicitly make spec.has_location False and __file__ missing with a non-list __path__ -> ignored."""
    test_module = import_module('migrations.test_migrations')

    class CustomPathIter(object):

        def __init__(self, seq):
            self._s = list(seq)

        def __iter__(self):
            return iter(self._s)
    custom = CustomPathIter(test_module.__path__)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=custom, modify_file='del')
    self.assertEqual(migrations, [])
    self.assertIn('migrations', unmigrated)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_original_path_restored_after_changes(self):
    """Ensure modifications to __path__/__file__ are properly restored after load_disk()."""
    test_module = import_module('migrations.test_migrations')
    orig_path = list(test_module.__path__)
    orig_file = getattr(test_module, '__file__', None)
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=tuple(orig_path), modify_file='del')
    self.assertEqual(list(test_module.__path__), orig_path)
    if orig_file is None:
        self.assertFalse(hasattr(test_module, '__file__'))
    else:
        self.assertEqual(test_module.__file__, orig_file)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_non_string_elements_in_list_path_still_treated_as_list_package(self):
    """If __path__ is a list instance (even with non-string elements) it is treated as a package; we must avoid TypeErrors."""
    test_module = import_module('migrations.test_migrations')

    class PathLike(str):
        pass
    orig = list(test_module.__path__)
    new_path = [PathLike(p) for p in orig]
    migrations, unmigrated, migrated = _get_migrations_for_module_state(modify_path=new_path, modify_file='del')
    self.assertCountEqual(migrations, ['0001_initial', '0002_second'])

from types import ModuleType
import sys
import pkgutil
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.apps import apps
from types import ModuleType
import sys
import pkgutil
from unittest.mock import patch
from django.test import TestCase, override_settings
from django.apps import apps
from django.db.migrations.loader import MigrationLoader

def make_submodule(fullname):
    mod = ModuleType(fullname)
    mod.Migration = DummyMigration
    return mod