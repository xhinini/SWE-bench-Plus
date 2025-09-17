from decimal import Decimal
import datetime
from django.test import TestCase
from django.db.models import Avg, Sum, Min, Publisher, Book
from .tests import AggregateTestCase