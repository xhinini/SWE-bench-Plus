from django.db import connection
from django.db.models import AutoField, BigAutoField, SmallAutoField, IntegerField, BigIntegerField, SmallIntegerField, CharField, UUIDField, SlugField, DecimalField, Model
from django.test import TransactionTestCase, skipUnlessDBFeature
from django.test.utils import isolate_apps
import unittest