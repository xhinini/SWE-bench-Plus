from decimal import Decimal
from django.db.models import Avg, Sum, Case, When
from django.test import TestCase
from .tests import aggregation as _agg_tests
from .tests.aggregation.tests import AggregateTestCase