from types import SimpleNamespace
from datetime import timedelta, timezone as dt_timezone
import pytz
from django.conf import settings
from django.test import override_settings
from django.utils import timezone
from django.db.models.fields import DateTimeField, DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime