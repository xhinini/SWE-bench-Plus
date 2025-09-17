from django import get_version
from django.conf import settings
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter
from django.test import SimpleTestCase
import datetime
import time
import uuid
import pathlib
import custom_migration_operations.more_operations
import custom_migration_operations.operations