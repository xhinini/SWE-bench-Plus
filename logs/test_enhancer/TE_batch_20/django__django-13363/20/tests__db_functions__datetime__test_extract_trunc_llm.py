from django.test import SimpleTestCase, override_settings
from django.utils import timezone
from django.db.models import F
import pytz
from django.db.models.functions import TruncDate, TruncTime