from math import ceil
from django.db import connection
from django.test import override_settings, skipUnlessDBFeature
from django.db.models import Value
from django.db.models.functions import Lower
from .models import Country, TwoFields