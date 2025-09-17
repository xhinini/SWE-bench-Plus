from unittest import mock
import datetime
import time
import uuid
from django.conf import settings
from django.test import SimpleTestCase
from django import get_version
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter, OperationWriter
import custom_migration_operations.operations