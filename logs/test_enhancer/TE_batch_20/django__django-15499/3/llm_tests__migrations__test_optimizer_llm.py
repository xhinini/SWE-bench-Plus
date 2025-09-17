from django.test import SimpleTestCase
from django.db import models, migrations
from django.db.migrations.optimizer import MigrationOptimizer
from .models import EmptyManager