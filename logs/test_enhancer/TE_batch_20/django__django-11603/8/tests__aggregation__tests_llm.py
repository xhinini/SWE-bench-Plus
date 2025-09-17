from decimal import Decimal
import datetime
from django.db import connection
from django.db.models import Avg, Sum, Count, Max, F, Value
from django.test.utils import CaptureQueriesContext
import datetime
from decimal import Decimal
from django.test import TestCase
from django.db import connection
from django.db.models import Avg, Sum, Count, Max, F, Value
from django.test.utils import CaptureQueriesContext
from .models import Author, Book, Publisher