from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Case, When
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Case, When
from .tests import AggregateTestCase
from .models import Book