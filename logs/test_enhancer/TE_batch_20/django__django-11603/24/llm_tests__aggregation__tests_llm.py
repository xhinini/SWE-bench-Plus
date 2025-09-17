from datetime import date
from decimal import Decimal
from django.db import connection
from django.test.utils import CaptureQueriesContext
from datetime import date
from decimal import Decimal
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from .models import Author, Book, Publisher
from django.db.models import Avg, Sum