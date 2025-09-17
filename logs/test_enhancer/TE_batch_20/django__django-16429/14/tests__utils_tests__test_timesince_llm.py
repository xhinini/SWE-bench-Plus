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

import datetime
from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

@requires_tz_support
@override_settings(USE_TZ=True)
class TZAwarePivotTimesinceAdditionalTests(TestCase):

    def setUp(self):
        self.tz1 = timezone.get_fixed_timezone(120)
        self.tz2 = timezone.get_fixed_timezone(195)

import datetime
from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

@requires_tz_support
@override_settings(USE_TZ=True)
class TimesincePivotTZTests(TestCase):

    def setUp(self):
        self.tz1 = timezone.get_fixed_timezone(60)
        self.tz2 = timezone.get_fixed_timezone(-330)

import datetime
from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil
import datetime
from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

@requires_tz_support
@override_settings(USE_TZ=True)
class TimesincePivotTzTests(TestCase):

    def setUp(self):
        self.tz_0 = timezone.get_fixed_timezone(0)
        self.tz_p60 = timezone.get_fixed_timezone(60)
        self.tz_p330 = timezone.get_fixed_timezone(330)
        self.tz_m120 = timezone.get_fixed_timezone(-120)

import datetime
from django.test import TestCase
from django.test.utils import override_settings, requires_tz_support
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

@requires_tz_support
@override_settings(USE_TZ=True)
class AdditionalTZAwareTimesinceTests(TestCase):

    def setUp(self):
        self.tz = timezone.get_fixed_timezone(0)