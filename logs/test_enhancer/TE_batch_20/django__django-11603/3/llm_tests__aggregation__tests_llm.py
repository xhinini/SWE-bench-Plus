from decimal import Decimal
from django.db.models import Avg, Sum, Count, F
from django.test import TestCase
from .tests import aggregation_tests as _unused
from .models import Book, Author, Publisher
from django.db.models.aggregates import Aggregate
from django.db.models.expressions import Star