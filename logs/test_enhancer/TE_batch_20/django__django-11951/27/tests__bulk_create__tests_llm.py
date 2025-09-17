from django.db.models.query import QuerySet
from math import ceil
from django.db import NotSupportedError, connection
from django.test import TestCase, override_settings
from django.db.models.query import QuerySet
from .models import TwoFields, Country, State