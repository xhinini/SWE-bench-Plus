from math import ceil
from django.db import connection
from django.test import skipUnlessDBFeature, skipIfDBFeature
from .models import TwoFields, Country, State, Restaurant