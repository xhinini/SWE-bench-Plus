from django.db import connection
from django.db.models import Avg, Sum, Max, Min, Count, F, Case, When
from django.test.utils import CaptureQueriesContext