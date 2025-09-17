from unittest.mock import patch
from math import ceil
from unittest.mock import patch
from django.db import connection
from django.test import skipUnlessDBFeature, skipIfDBFeature, override_settings
from .models import TwoFields, Restaurant