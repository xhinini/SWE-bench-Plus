from datetime import datetime, timedelta, timezone as dt_timezone
import pytz
from django.conf import settings
from django.db.models import DateField, DateTimeField, TimeField, Subquery, OuterRef, Max
from django.db.models.functions import TruncDate, TruncTime, TruncYear
from django.test import TestCase, override_settings
from django.utils import timezone
from ..models import DTModel, Author, Fan