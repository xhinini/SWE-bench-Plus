import pytz
from django.utils import timezone
from datetime import timedelta, timezone as datetime_timezone
import pytz
from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from django.db.models.fields import DateField, DateTimeField, TimeField
from django.db.models.functions import TruncDate, TruncTime