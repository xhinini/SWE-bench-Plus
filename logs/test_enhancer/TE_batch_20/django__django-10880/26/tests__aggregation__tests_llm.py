from django.db import connection
from django.db.models import Count, Case, When
from django.test.utils import CaptureQueriesContext
from django.db.models import Q