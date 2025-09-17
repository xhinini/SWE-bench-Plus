from unittest.mock import patch
from math import ceil
from unittest.mock import patch
from django.db import connection
from django.test import TestCase, skipUnlessDBFeature
from .models import Country, State, TwoFields, NoFields, Restaurant