from django.db import connection
from django.test import TransactionTestCase
from .tests import SchemaTests
from .models import Author
from django.db.models import IntegerField, CharField, BinaryField, FloatField, DecimalField, TextField, UUIDField, DateField, DurationField, SmallIntegerField