from decimal import Decimal
from django.test import TestCase
from django.db.models import Avg, Sum, Case, When, Max
from django.test.utils import Approximate
from .tests import AggregateTestCase as _AggregateTestCase