from django.db import migrations, models
from django.db.migrations import operations
from django.db.migrations import optimizer as optimizer_module
from django.db.migrations.optimizer import MigrationOptimizer
from django.test import SimpleTestCase
from .models import EmptyManager, UnicodeModel