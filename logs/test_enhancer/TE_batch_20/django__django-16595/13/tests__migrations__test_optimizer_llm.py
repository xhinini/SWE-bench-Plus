from django.db import migrations, models
from django.db.migrations import operations
from django.db.migrations.operations.fields import AlterField, RemoveField, RenameField
from django.db.migrations.optimizer import MigrationOptimizer
from django.test import SimpleTestCase