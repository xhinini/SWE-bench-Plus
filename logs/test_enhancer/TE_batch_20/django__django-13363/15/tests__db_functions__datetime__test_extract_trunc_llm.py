from datetime import timedelta, timezone as datetime_timezone
import pytz
from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db.models import DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime
from ..models import DTModel