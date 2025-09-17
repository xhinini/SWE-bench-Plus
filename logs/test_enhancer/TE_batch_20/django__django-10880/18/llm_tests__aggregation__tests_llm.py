from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count
from django.db.models.expressions import Case, When