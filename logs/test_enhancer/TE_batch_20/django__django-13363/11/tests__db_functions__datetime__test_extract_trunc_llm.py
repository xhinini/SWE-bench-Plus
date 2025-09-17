from django.utils import timezone
from django.db.models.fields import DateTimeField
import pytz
from datetime import timezone as dt_timezone, timedelta
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.conf import settings
from django.db.models.fields import DateTimeField
from django.db.models.functions import TruncDate, TruncTime