from django import get_version
from django.conf import settings
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter
from django.test import SimpleTestCase
import datetime
import decimal
import pathlib
import time
import uuid
import custom_migration_operations.more_operations
import custom_migration_operations.operations