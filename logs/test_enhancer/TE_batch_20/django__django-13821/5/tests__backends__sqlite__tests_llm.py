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