from decimal import Decimal
import datetime
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.db.models import Avg, Sum, F
from django.db.models import Value
from django.db.models.functions import Cast
from .models import Book, Publisher