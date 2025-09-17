from unittest.mock import Mock
import pytz
from django.utils import timezone as dj_timezone
from unittest.mock import Mock
from datetime import timezone as dt_timezone
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone as dj_timezone
from django.db.models.functions import TruncDate, TruncTime