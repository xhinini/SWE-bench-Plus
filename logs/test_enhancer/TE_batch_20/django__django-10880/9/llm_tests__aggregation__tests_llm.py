from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Value, F
import re
from .models import Book
from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.db.models import Count, Value, F
import re
from .models import Book