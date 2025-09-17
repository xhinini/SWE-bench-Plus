from datetime import timezone as dt_timezone, timedelta
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db.models import F
from django.db.models.functions import TruncDate, TruncTime