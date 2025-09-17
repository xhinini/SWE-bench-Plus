from unittest import mock
import types
from unittest import mock
from django.test import TestCase
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.exceptions import BadMigrationError
from django.db.migrations.recorder import MigrationRecorder