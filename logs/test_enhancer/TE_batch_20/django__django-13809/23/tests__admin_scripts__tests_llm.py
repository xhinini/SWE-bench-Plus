from io import StringIO
from unittest import mock
from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import RunserverCommand
from django.db.migrations.recorder import MigrationRecorder
from django.test import SimpleTestCase, override_settings