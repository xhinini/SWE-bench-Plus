from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil
import datetime

@requires_tz_support
@override_settings(USE_TZ=True)
class TZAwarePivotTimesinceTests(TestCase):

    def setUp(self):
        self.tz_default = timezone.get_default_timezone()
        self.tz_fixed = timezone.get_fixed_timezone(195)