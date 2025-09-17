from django.db import connection
from django.db.models import Count, Max, Case, When
from django.test.utils import CaptureQueriesContext
from .models import Book
from .tests import AggregateTestCase as _BaseAggregateTestCase