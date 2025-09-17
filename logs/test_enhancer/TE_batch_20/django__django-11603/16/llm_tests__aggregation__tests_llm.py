from decimal import Decimal
import datetime
from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Avg, Sum, Count
from .models import Book, Author, Publisher