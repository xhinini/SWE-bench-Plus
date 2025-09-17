from datetime import timedelta
from django.db.models import DurationField
from datetime import timedelta
from django.db.models import Avg, Sum, F, DurationField
from django.test import TestCase
from django.core.exceptions import TypeError as CoreTypeError
from .models import Book, Publisher