import io
import types
from unittest import mock
from django.core.management import call_command
from django.test import TestCase
EXECUTOR_PATH = 'django.core.management.commands.sqlmigrate.MigrationExecutor'