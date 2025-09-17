from django.db.models import Avg, Sum, Count, Case, When, F, DurationField
from django.test.utils import CaptureQueriesContext
from datetime import timedelta
from decimal import Decimal
from django.db import connection
from django.db.models import Avg, Sum, Count, Case, When, F, DurationField
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from .models import Book, Publisher