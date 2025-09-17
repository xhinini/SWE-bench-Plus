import pytz
from django.utils import timezone
from datetime import datetime, time
import pytz
from django.conf import settings
from django.db.models import DateField, TimeField, DateTimeField, Count
from django.db.models.functions import TruncDate, TruncTime, TruncYear
from django.test import TestCase, override_settings
from django.utils import timezone
from ..models import DTModel, Author, Fan