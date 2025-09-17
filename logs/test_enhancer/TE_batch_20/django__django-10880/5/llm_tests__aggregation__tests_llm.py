from django.db import connection
from django.test.utils import CaptureQueriesContext
from .tests import AggregateTestCase
from .models import Book
from django.db.models import Count, Sum, Case, When