import importlib
import sys
import unittest
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
import importlib
import sys
import unittest
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
MODULE_NAME = 'django.db.backends.sqlite3.base'
try:
    base_mod = importlib.import_module(MODULE_NAME)
except ImproperlyConfigured:
    base_mod = sys.modules.get(MODULE_NAME)
if __name__ == '__main__':
    unittest.main()