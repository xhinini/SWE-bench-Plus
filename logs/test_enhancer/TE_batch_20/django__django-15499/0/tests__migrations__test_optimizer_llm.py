from django.test import SimpleTestCase
from django.db import migrations, models
from django.db.migrations import operations
from django.db.migrations.optimizer import MigrationOptimizer
from django.db.migrations.serializer import serializer_factory

def _serialize(op):
    return serializer_factory(op).serialize()[0]