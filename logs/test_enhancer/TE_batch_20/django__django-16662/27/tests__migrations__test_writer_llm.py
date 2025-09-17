from django import get_version
import datetime
import time
import os
from django.test import SimpleTestCase
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter
import custom_migration_operations.operations
import custom_migration_operations.more_operations
new_imports_code: ''