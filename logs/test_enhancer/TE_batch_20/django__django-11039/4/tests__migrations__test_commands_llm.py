from django.core.management.commands.sqlmigrate import Command
from django.db import connections, connection
import io
from unittest import mock
from django.core.management import call_command
from django.test import override_settings
from django.db import connections, connection
from django.core.management.commands.sqlmigrate import Command
import io
from unittest import mock
from .test_base import MigrationTestBase