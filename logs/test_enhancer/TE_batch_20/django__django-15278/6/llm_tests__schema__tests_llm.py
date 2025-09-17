import unittest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.test import TransactionTestCase
from django.db.models import AutoField, BigAutoField, SmallAutoField, IntegerField, BigIntegerField, CharField, SlugField, UUIDField, DecimalField, BooleanField
from .models import Author