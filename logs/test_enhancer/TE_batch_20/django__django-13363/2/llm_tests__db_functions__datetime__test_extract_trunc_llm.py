from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.test import override_settings, TestCase
from django.utils import timezone
from django.db.models import DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime
from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.test import override_settings, TestCase
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncTime
from django.db.models import DateField, TimeField
from ..models import DTModel