from unittest.mock import patch
from math import ceil
from django.db import connections, connection
from django.db.models.query import QuerySet
from django.test import TestCase, skipUnlessDBFeature
from django.db import IntegrityError
from unittest.mock import patch
from math import ceil
from .models import TwoFields