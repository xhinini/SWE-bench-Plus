import os
import re
from types import SimpleNamespace
from unittest import mock
from django import get_version
from django.conf import settings
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter
from django.test import SimpleTestCase
from django.utils.timezone import now