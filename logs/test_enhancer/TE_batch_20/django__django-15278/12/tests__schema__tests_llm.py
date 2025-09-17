from django.db.models import BinaryField
from django.db import IntegrityError, connection
from django.db.models import AutoField, CharField, IntegerField, BinaryField, OneToOneField
from django.test.utils import CaptureQueriesContext
from django.test import TransactionTestCase
from .tests import SchemaTests
from .models import Author, Note