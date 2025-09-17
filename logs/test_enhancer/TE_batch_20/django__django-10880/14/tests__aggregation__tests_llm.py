from django.db import connection
from django.db.models import Count, F, Case, When
from django.test.utils import CaptureQueriesContext