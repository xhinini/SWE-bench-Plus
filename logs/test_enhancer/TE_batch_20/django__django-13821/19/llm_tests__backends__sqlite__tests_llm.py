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