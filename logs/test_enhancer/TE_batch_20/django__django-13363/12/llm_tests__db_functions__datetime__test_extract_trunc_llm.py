from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.conf import settings
from django.db.models import DateTimeField, Subquery, Max
from django.db.models.functions import TruncDate, TruncTime
from django.test import override_settings
from django.utils import timezone
from ..models import DTModel, Author, Fan