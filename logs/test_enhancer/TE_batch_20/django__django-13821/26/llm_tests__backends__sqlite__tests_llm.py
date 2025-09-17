import importlib
import sys
from sqlite3 import dbapi2 as dbapi
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
import importlib
import sys
import unittest
from sqlite3 import dbapi2 as dbapi
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from unittest import skipUnless
skip_if_not_sqlite = skipUnless(connection.vendor == 'sqlite', 'SQLite tests')

def _reload_base_module_under_patched_dbapi(version_info, version_string):
    """
    Remove the module from sys.modules and import it while sqlite3.dbapi2's
    attributes are patched to the provided values. Return the imported module
    (if successful) or raise the exception from the import.
    """
    module_name = 'django.db.backends.sqlite3.base'
    sys.modules.pop(module_name, None)
    with mock.patch.object(dbapi, 'sqlite_version_info', version_info), mock.patch.object(dbapi, 'sqlite_version', version_string):
        return importlib.import_module(module_name)
if __name__ == '__main__':
    unittest.main()

import importlib
import sys
from sqlite3 import dbapi2 as Database
from unittest import mock
import importlib
import sys
import unittest
from sqlite3 import dbapi2 as Database
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
MODULE_PATH = 'django.db.backends.sqlite3.base'

class SQLiteVersionCheckTests(unittest.TestCase):

    def setUp(self):
        self.base = importlib.import_module(MODULE_PATH)
if __name__ == '__main__':
    unittest.main()

import importlib
import sys
import sys
import importlib
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

def import_sqlite_base_module():
    module_name = 'django.db.backends.sqlite3.base'
    sys.modules.pop(module_name, None)
    return importlib.import_module(module_name)

import importlib
import sys
import re
import sys
import importlib
import unittest
from sqlite3 import dbapi2 as Database
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
import re
MODULE_PATH = 'django.db.backends.sqlite3.base'

class SQLiteVersionRequirementTests(unittest.TestCase):

    def setUp(self):
        try:
            self.module = importlib.import_module(MODULE_PATH)
        except ImproperlyConfigured:
            sys.modules.pop(MODULE_PATH, None)
            self.module = importlib.import_module(MODULE_PATH)
if __name__ == '__main__':
    unittest.main()

import unittest
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.test import TestCase

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite tests')
class SQLiteVersionRequirementTests(TestCase):
    longMessage = True

    def _call_check(self):
        from django.db.backends.sqlite3.base import check_sqlite_version
        return check_sqlite_version

import importlib
import sys
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
import unittest
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
import importlib
import sys
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
import unittest
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite tests')
class CheckSQLiteVersionExtraTests(unittest.TestCase):

    def _load_module_safely(self):
        """
        Load the module under a safe (>= 3.9.0) version to get access to the
        check_sqlite_version function for direct calls in other tests.
        """
        return self._reload_module_with_version((3, 9, 0), '3.9.0')

import importlib
import sys

def test_check_sqlite_version_3_8_4_raises(self):
    msg = 'SQLite 3.9.0 or later is required (found 3.8.4).'
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 8, 4)), mock.patch.object(dbapi2, 'sqlite_version', '3.8.4'), self.assertRaisesMessage(ImproperlyConfigured, msg):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_3_8_3_raises(self):
    msg = 'SQLite 3.9.0 or later is required (found 3.8.3).'
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 8, 3)), mock.patch.object(dbapi2, 'sqlite_version', '3.8.3'), self.assertRaisesMessage(ImproperlyConfigured, msg):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_3_8_11_1_raises_and_message_contains_version(self):
    msg = 'SQLite 3.9.0 or later is required (found 3.8.11.1).'
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 8, 11, 1)), mock.patch.object(dbapi2, 'sqlite_version', '3.8.11.1'), self.assertRaisesMessage(ImproperlyConfigured, msg):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_short_tuple_3_9_raises(self):
    msg = 'SQLite 3.9.0 or later is required (found 3.9).'
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 9)), mock.patch.object(dbapi2, 'sqlite_version', '3.9'), self.assertRaisesMessage(ImproperlyConfigured, msg):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_exact_3_9_0_ok(self):
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 9, 0)), mock.patch.object(dbapi2, 'sqlite_version', '3.9.0'):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_higher_version_ok(self):
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 10, 1)), mock.patch.object(dbapi2, 'sqlite_version', '3.10.1'):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_extra_long_tuple_ok(self):
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (4, 0, 0, 0)), mock.patch.object(dbapi2, 'sqlite_version', '4.0.0.0'):
        sqlite3_backend.base.check_sqlite_version()

def test_check_sqlite_version_non_tuple_raises_typeerror(self):
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', '3.8.5'), mock.patch.object(dbapi2, 'sqlite_version', '3.8.5'), self.assertRaises(TypeError):
        sqlite3_backend.base.check_sqlite_version()

def test_import_time_check_raises_on_old_version(self):
    import importlib, sys
    module_name = 'django.db.backends.sqlite3.base'
    if module_name in sys.modules:
        del sys.modules[module_name]
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 8, 5)), mock.patch.object(dbapi2, 'sqlite_version', '3.8.5'), self.assertRaises(ImproperlyConfigured):
        try:
            importlib.import_module(module_name)
        finally:
            if module_name in sys.modules:
                del sys.modules[module_name]

def test_check_sqlite_version_3_8_5_raises(self):
    msg = 'SQLite 3.9.0 or later is required (found 3.8.5).'
    from django.db.backends import sqlite3 as sqlite3_backend
    with mock.patch.object(dbapi2, 'sqlite_version_info', (3, 8, 5)), mock.patch.object(dbapi2, 'sqlite_version', '3.8.5'), self.assertRaisesMessage(ImproperlyConfigured, msg):
        sqlite3_backend.base.check_sqlite_version()

import importlib
import sys
import unittest
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
import importlib
import sys
import unittest
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
MODULE_NAME = 'django.db.backends.sqlite3.base'

def _reload_base_module():
    """
    Helper to force re-import of the sqlite base module.
    """
    sys.modules.pop(MODULE_NAME, None)
    sys.modules.pop('django.db.backends.sqlite3', None)
    return importlib.import_module(MODULE_NAME)

import importlib
import sys
import re
from sqlite3 import dbapi2 as Database
from unittest import mock
import importlib
import sys
import re
import unittest
from sqlite3 import dbapi2 as Database
from django.core.exceptions import ImproperlyConfigured
from unittest import mock
MODULE_NAME = 'django.db.backends.sqlite3.base'

class SQLiteVersionCheckTests(unittest.TestCase):

    def setUp(self):
        self.original_module = sys.modules.get(MODULE_NAME)
        if MODULE_NAME in sys.modules:
            del sys.modules[MODULE_NAME]

    def tearDown(self):
        if MODULE_NAME in sys.modules:
            del sys.modules[MODULE_NAME]
        if self.original_module is not None:
            sys.modules[MODULE_NAME] = self.original_module
if __name__ == '__main__':
    unittest.main()