import importlib
import sys
from sqlite3 import dbapi2 as Database
from unittest import mock
from django.db import connection
from django.core.exceptions import ImproperlyConfigured
import unittest
import importlib
import sys
from sqlite3 import dbapi2 as Database
from unittest import mock
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
MODULE_NAME = 'django.db.backends.sqlite3.base'