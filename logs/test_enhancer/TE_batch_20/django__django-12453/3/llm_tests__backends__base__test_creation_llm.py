from unittest import mock
from unittest import mock
from django.core import serializers
from django.db import connection
from django.test import SimpleTestCase
from django.db.backends.base.creation import BaseDatabaseCreation
from tests.backends.base.test_creation import get_connection_copy