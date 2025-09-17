import unittest
from sqlite3 import dbapi2
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.db.backends.sqlite3 import base