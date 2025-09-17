import decimal
import datetime
import time
import uuid
import pathlib
from django.conf import SettingsReference, settings
from django.db import migrations, models
from django.test import SimpleTestCase
from django.utils.timezone import utc
from django.db.migrations.writer import MigrationWriter