from django.db import connection
from django.db.models import Count
from django.test.utils import CaptureQueriesContext
from .tests import AggregateTestCase
from .models import Book, Author
from django.db import connection
from django.db.models import Count
from django.test.utils import CaptureQueriesContext
from .tests import AggregateTestCase
from .models import Book, Author