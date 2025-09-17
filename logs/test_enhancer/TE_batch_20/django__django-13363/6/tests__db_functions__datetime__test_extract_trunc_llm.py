from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.conf import settings
from django.test import override_settings
from django.utils import timezone
from django.db.models import DateField, TimeField
from ..models import DTModel
from django.db.models.functions import TruncDate, TruncTime