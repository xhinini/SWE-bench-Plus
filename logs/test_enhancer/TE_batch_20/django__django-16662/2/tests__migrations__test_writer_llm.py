from django.db.migrations.serializer import BaseSerializer
from unittest import mock
import datetime
import re
from django.db import migrations, models
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter
from django.test import SimpleTestCase