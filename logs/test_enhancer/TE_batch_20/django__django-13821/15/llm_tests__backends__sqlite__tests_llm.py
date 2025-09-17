import importlib
import sys
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
import importlib
import sys
import unittest
from sqlite3 import dbapi2 as dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
try:
    from django.db.backends.sqlite3.base import check_sqlite_version
except ImproperlyConfigured:
    check_sqlite_version = None
if __name__ == '__main__':
    unittest.main()