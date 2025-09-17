import importlib
import sys
from sqlite3 import dbapi2
from unittest import mock
import importlib
import sys
from sqlite3 import dbapi2
from unittest import mock
import unittest
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.test import TestCase
try:
    from django.db.backends.sqlite3.base import check_sqlite_version
    SKIP_CHECK = False
except ImproperlyConfigured:
    check_sqlite_version = None
    SKIP_CHECK = True