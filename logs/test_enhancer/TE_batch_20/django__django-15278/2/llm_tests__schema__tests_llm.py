import unittest
from django.db import connection
from django.db.transaction import TransactionManagementError
from django.test.utils import CaptureQueriesContext
from django.test import skipUnlessDBFeature
from .models import Author
from django.db.models import AutoField, BigAutoField, SmallAutoField, IntegerField, UUIDField, CharField
from django.test import skipUnlessDBFeature
import unittest