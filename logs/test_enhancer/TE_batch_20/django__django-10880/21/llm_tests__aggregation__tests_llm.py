import re
from decimal import Decimal
from django.db import connection
from django.db.models import Count, Case, When, Value
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from .models import Author, Book, Publisher