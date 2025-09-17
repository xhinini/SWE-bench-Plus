from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Case, When, F, Q
from .models import Book