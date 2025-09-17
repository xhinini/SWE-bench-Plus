import pytz
from datetime import datetime, timedelta, timezone as dt_timezone
from django.utils import timezone
from django.test import override_settings
from datetime import datetime, timedelta, timezone as dt_timezone
import pytz
from django.utils import timezone
from django.test import override_settings
from ..models import DTModel
from django.db.models.functions import TruncDate, TruncTime