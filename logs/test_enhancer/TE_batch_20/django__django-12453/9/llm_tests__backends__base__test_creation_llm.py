from contextlib import contextmanager
from unittest import mock
from django.db import connection
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db import connections, DEFAULT_DB_ALIAS
from .test_creation import get_connection_copy
new_imports_code: ''