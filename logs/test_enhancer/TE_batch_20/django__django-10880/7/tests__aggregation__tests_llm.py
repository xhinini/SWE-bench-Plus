from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.db.models import Count, Sum, F, Case, When, Value
from .models import Book
from .tests import AggregateTestCase