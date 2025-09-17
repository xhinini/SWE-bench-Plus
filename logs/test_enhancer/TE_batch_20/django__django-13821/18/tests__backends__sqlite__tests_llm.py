import importlib
import sys
from sqlite3 import dbapi2 as dbapi2_module
from unittest import mock
import importlib
import sys
import unittest
from sqlite3 import dbapi2 as dbapi2_module
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.test import TestCase
try:
    from django.db.backends.sqlite3 import base as sqlite_base_module
    check_sqlite_version = sqlite_base_module.check_sqlite_version
except ImproperlyConfigured:
    sqlite_base_module = None
    check_sqlite_version = None