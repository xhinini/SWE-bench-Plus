from unittest.mock import patch
from math import ceil
from operator import attrgetter
from unittest.mock import patch
from django.db import connection
from django.test import skipUnlessDBFeature
from .models import TwoFields, Country