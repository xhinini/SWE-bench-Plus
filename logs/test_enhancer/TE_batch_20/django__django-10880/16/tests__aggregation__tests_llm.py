from unittest import mock
from django.db import connection
from django.db.models import Case, Count, Value, When
from django.test.utils import CaptureQueriesContext
from unittest import mock
from django.db import connection
from django.db.models import Case, Count, Value, When
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from .models import Book