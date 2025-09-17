from django.utils import timezone
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.conf import settings
import pytz
from django.db.models.fields import DateTimeField, TimeField
from django.db.models.functions import TruncDate, TruncTime