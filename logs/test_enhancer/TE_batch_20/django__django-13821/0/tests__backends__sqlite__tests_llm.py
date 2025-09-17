from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from __future__ import annotations
import datetime
import unittest
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from django.db.backends.sqlite3.base import check_sqlite_version, SQLiteCursorWrapper, _sqlite_format_dtdelta, _sqlite_time_diff, _sqlite_timestamp_diff