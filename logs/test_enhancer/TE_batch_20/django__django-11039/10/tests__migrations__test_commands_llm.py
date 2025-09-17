from django.test import override_settings
from django.core.management import call_command
from django.db import connections, connection
import io
from unittest import mock
from .test_base import MigrationTestBase