from django.test import SimpleTestCase
from django.db.migrations.writer import MigrationWriter
from django.db.migrations.serializer import BaseSerializer
import custom_migration_operations.operations