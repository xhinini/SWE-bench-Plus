from unittest.mock import patch
from math import ceil
from unittest.mock import patch
from django.db import connection
from django.test import skipUnlessDBFeature
from .models import Country, TwoFields, Restaurant, NoFields