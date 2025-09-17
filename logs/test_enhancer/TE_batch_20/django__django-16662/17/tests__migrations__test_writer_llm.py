import datetime
import time
import uuid
from django import get_version
from django.conf import settings
from django.db import migrations, models
from django.test import SimpleTestCase
from django.db.migrations.writer import MigrationWriter
from django.conf import SettingsReference
try:
    from migrations.test_writer import Money
except Exception:
    import decimal

    class Money(decimal.Decimal):

        def deconstruct(self):
            return ('%s.%s' % (self.__class__.__module__, self.__class__.__name__), [str(self)], {})