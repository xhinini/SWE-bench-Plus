from django.db import connection
from django.db.models import Count, Case, When, F, IntegerField
from django.test.utils import CaptureQueriesContext