import io
from unittest import mock
from unittest import mock
import io
from django.core.management import call_command
from django.test import override_settings
from .test_base import MigrationTestBase
from django.db import connections, connection