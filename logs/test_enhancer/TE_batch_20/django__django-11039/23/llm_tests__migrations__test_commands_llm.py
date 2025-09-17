from django.core.management.commands.sqlmigrate import Command
from django.core.management import call_command
from django.core.management.commands.sqlmigrate import Command
from django.db import connection, connections
from django.test import override_settings
from unittest import mock
import io
from .test_base import MigrationTestBase