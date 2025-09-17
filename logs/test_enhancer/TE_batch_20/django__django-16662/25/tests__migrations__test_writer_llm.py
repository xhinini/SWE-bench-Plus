from __future__ import annotations
import types
from typing import Set, Tuple
from django.test import SimpleTestCase
from django.db import migrations
from django.db.migrations.writer import MigrationWriter
from django.db.migrations.serializer import BaseSerializer