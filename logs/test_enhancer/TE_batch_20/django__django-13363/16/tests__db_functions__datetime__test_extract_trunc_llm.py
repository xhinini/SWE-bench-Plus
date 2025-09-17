import types
from django.utils import timezone as django_timezone
from django.db.models.functions import TruncDate, TruncTime
from django.db.models.fields import DateTimeField, TimeField, DateField

def _make_dummy_connection(capture, sql_prefix='SQL'):
    """
    Create a dummy connection with ops implementing datetime_cast_date_sql
    and datetime_cast_time_sql. These methods record the tzname passed
    into the supplied capture dict and return a simple SQL string.
    """

    class Ops:

        def datetime_cast_date_sql(self, lhs, tzname):
            capture['tzname'] = tzname
            return f'{sql_prefix}_DATE({lhs})'

        def datetime_cast_time_sql(self, lhs, tzname):
            capture['tzname'] = tzname
            return f'{sql_prefix}_TIME({lhs})'

    class Features:
        has_zoneinfo_database = True
    return types.SimpleNamespace(ops=Ops(), features=Features())

def test_truncdate_uses_explicit_tzinfo_over_current_timezone(self):
    """
    When a tzinfo is passed to TruncDate, the tzname passed to
    connection.ops.datetime_cast_date_sql must be obtained via the instance
    (i.e. self.get_tzname()) and not the current timezone.
    """
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    melb = pytz.timezone('Australia/Melbourne')
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=melb)
    with django_timezone.override(pytz.UTC):
        tzname, sql_params = (None, None)
        sql, params = trunc.as_sql(dummy_compiler, conn)
        tzname = capture.get('tzname')
    expected = trunc.get_tzname()
    assert tzname == expected, 'TruncDate should use explicit tzinfo over current timezone'

def test_trunctime_uses_explicit_tzinfo_over_current_timezone(self):
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    pacific = pytz.timezone('US/Pacific')
    trunc = TruncTime(_DummyExpr(output_field=DateTimeField()), tzinfo=pacific)
    with django_timezone.override(pytz.UTC):
        sql, params = trunc.as_sql(dummy_compiler, conn)
        tzname = capture.get('tzname')
    expected = trunc.get_tzname()
    assert tzname == expected, 'TruncTime should use explicit tzinfo over current timezone'

def test_truncdate_uses_current_timezone_when_no_explicit_tz(self):
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=None)
    with django_timezone.override(pytz.timezone('Australia/Sydney')):
        sql, params = trunc.as_sql(dummy_compiler, conn)
        tzname = capture.get('tzname')
    expected = trunc.get_tzname()
    assert tzname == expected, 'TruncDate with no explicit tzinfo must use current timezone name'

def test_trunctime_uses_current_timezone_when_no_explicit_tz(self):
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    trunc = TruncTime(_DummyExpr(output_field=DateTimeField()), tzinfo=None)
    with django_timezone.override(pytz.timezone('Europe/Paris')):
        sql, params = trunc.as_sql(dummy_compiler, conn)
        tzname = capture.get('tzname')
    expected = trunc.get_tzname()
    assert tzname == expected, 'TruncTime with no explicit tzinfo must use current timezone name'

def test_truncdate_with_fixed_offset_tzinfo(self):
    """
    For tzinfo values that are fixed offsets (datetime.timezone), get_tzname()
    must be used and its result propagated to the backend.
    """
    capture = {}
    conn = _make_dummy_connection(capture)
    offset = datetime_timezone(timedelta(hours=-5, minutes=-30))
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=offset)
    sql, params = trunc.as_sql(dummy_compiler, conn)
    tzname = capture.get('tzname')
    assert tzname == trunc.get_tzname(), 'TruncDate should propagate get_tzname() for fixed offset tzinfo'

@override_settings(USE_TZ=False)
def test_truncdate_ignores_tz_when_USE_TZ_false(self):
    """
    When USE_TZ is False, TruncDate.as_sql must pass tzname=None regardless
    of the tzinfo passed to the TruncDate instance.
    """
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    melb = pytz.timezone('Australia/Melbourne')
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=melb)
    sql, params = trunc.as_sql(dummy_compiler, conn)
    assert capture.get('tzname') is None, 'When USE_TZ=False, tzname passed must be None'

@override_settings(USE_TZ=False)
def test_trunctime_ignores_tz_when_USE_TZ_false(self):
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    pacific = pytz.timezone('US/Pacific')
    trunc = TruncTime(_DummyExpr(output_field=DateTimeField()), tzinfo=pacific)
    sql, params = trunc.as_sql(dummy_compiler, conn)
    assert capture.get('tzname') is None, 'When USE_TZ=False, tzname passed for TruncTime must be None'

def test_truncdate_honors_pytz_utc(self):
    """
    Explicit pytz.UTC tzinfo must be propagated via get_tzname().
    """
    capture = {}
    conn = _make_dummy_connection(capture)
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('col', []))
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=pytz.UTC)
    sql, params = trunc.as_sql(dummy_compiler, conn)
    assert capture.get('tzname') == trunc.get_tzname()

def test_truncdate_as_sql_returns_sql_and_params(self):
    """
    Ensure as_sql returns the SQL string returned by connection.ops and the
    parameters returned by the compiler.
    """
    capture = {}
    conn = _make_dummy_connection(capture, sql_prefix='RET')
    dummy_compiler = types.SimpleNamespace(compile=lambda expr: ('LHS', [42]))
    trunc = TruncDate(_DummyExpr(output_field=DateTimeField()), tzinfo=pytz.UTC)
    sql, params = trunc.as_sql(dummy_compiler, conn)
    assert sql == 'RET_DATE(LHS)', 'as_sql must return the SQL string returned by connection.ops'
    assert params == [42], 'as_sql must return the parameters provided by the compiler'

from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db.models import DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime
from ..models import DTModel
from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db.models import DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime
from ..models import DTModel

def _create_model(start_datetime, end_datetime):
    return DTModel.objects.create(name=start_datetime.isoformat() if start_datetime else 'None', start_datetime=start_datetime, end_datetime=end_datetime, start_date=start_datetime.date() if start_datetime else None, end_date=end_datetime.date() if end_datetime else None, start_time=start_datetime.time() if start_datetime else None, end_time=end_datetime.time() if end_datetime else None, duration=end_datetime - start_datetime if start_datetime and end_datetime else None)

from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.test import TestCase, override_settings
from django.utils import timezone
from django.db.models import DateField, TimeField
from django.db.models.functions import TruncDate, TruncTime
from ..models import DTModel

@override_settings(USE_TZ=True, TIME_ZONE='UTC')
class TruncExplicitTimezoneTests(TestCase):

    def _make_utc_dt(self, year=2023, month=1, day=1, hour=23, minute=0):
        dt = datetime(year, month, day, hour, minute)
        return timezone.make_aware(dt, is_dst=False)

from datetime import datetime, timedelta, timezone as datetime_timezone
import pytz
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncTime
from .test_extract_trunc import DateFunctionWithTimeZoneTests, DTModel

def _make_aware(dt):
    return timezone.make_aware(dt, is_dst=False)

def test_truncdate_respects_explicit_tzinfo(self):
    """
    TruncDate(..., tzinfo=tz) should return the date in the provided timezone,
    not the current timezone.
    """
    start = _make_aware(datetime(2023, 1, 1, 3, 0, 0))
    self.create_model(start, start)
    ny = pytz.timezone('America/New_York')
    obj = DTModel.objects.annotate(truncated=TruncDate('start_datetime', tzinfo=ny)).get()
    expected = start.astimezone(ny).date()
    self.assertEqual(obj.truncated, expected)

def test_trunctime_respects_explicit_tzinfo(self):
    """
    TruncTime(..., tzinfo=tz) should return the time in the provided timezone.
    """
    start = _make_aware(datetime(2023, 1, 1, 2, 30, 0))
    self.create_model(start, start)
    ny = pytz.timezone('America/New_York')
    obj = DTModel.objects.annotate(truncated=TruncTime('start_datetime', tzinfo=ny)).get()
    expected = start.astimezone(ny).time()
    self.assertEqual(obj.truncated, expected)

def test_truncdate_tzinfo_precedence_over_current_timezone(self):
    """
    When an explicit tzinfo is provided, it must be used even if the current
    timezone (timezone.override) is different.
    """
    start = _make_aware(datetime(2023, 1, 1, 4, 0, 0))
    self.create_model(start, start)
    ny = pytz.timezone('America/New_York')
    tokyo = pytz.timezone('Asia/Tokyo')
    with timezone.override(tokyo):
        obj = DTModel.objects.annotate(explicit=TruncDate('start_datetime', tzinfo=ny), implicit=TruncDate('start_datetime')).get()
    self.assertEqual(obj.explicit, start.astimezone(ny).date())
    self.assertEqual(obj.implicit, start.astimezone(tokyo).date())

def test_trunctime_tzinfo_precedence_over_current_timezone(self):
    """
    TruncTime with explicit tzinfo must be unaffected by timezone.override.
    """
    start = _make_aware(datetime(2023, 1, 1, 4, 15, 0))
    self.create_model(start, start)
    ny = pytz.timezone('America/New_York')
    tokyo = pytz.timezone('Asia/Tokyo')
    with timezone.override(tokyo):
        obj = DTModel.objects.annotate(explicit=TruncTime('start_datetime', tzinfo=ny), implicit=TruncTime('start_datetime')).get()
    self.assertEqual(obj.explicit, start.astimezone(ny).time())
    self.assertEqual(obj.implicit, start.astimezone(tokyo).time())

def test_truncdate_with_fixed_offset_tzinfo(self):
    """
    A fixed-offset tzinfo (datetime.timezone) should be honored by TruncDate.
    """
    start = _make_aware(datetime(2023, 1, 1, 1, 30, 0))
    self.create_model(start, start)
    fixed = datetime_timezone(timedelta(hours=-2))
    obj = DTModel.objects.annotate(truncated=TruncDate('start_datetime', tzinfo=fixed)).get()
    expected = start.astimezone(fixed).date()
    self.assertEqual(obj.truncated, expected)

def test_trunctime_with_fixed_offset_tzinfo(self):
    """
    A fixed-offset tzinfo should be honored by TruncTime.
    """
    start = _make_aware(datetime(2023, 1, 1, 1, 30, 45))
    self.create_model(start, start)
    fixed = datetime_timezone(timedelta(hours=3, minutes=30))
    obj = DTModel.objects.annotate(truncated=TruncTime('start_datetime', tzinfo=fixed)).get()
    expected = start.astimezone(fixed).time()
    self.assertEqual(obj.truncated, expected)

def test_truncdate_with_named_tz_and_override_different_current(self):
    """
    Ensure an explicitly named tzinfo (pytz timezone) is used even when the
    currently active timezone is different.
    """
    start = _make_aware(datetime(2023, 6, 1, 0, 30, 0))
    self.create_model(start, start)
    la = pytz.timezone('America/Los_Angeles')
    sydney = pytz.timezone('Australia/Sydney')
    with timezone.override(sydney):
        obj = DTModel.objects.annotate(explicit=TruncDate('start_datetime', tzinfo=la), implicit=TruncDate('start_datetime')).get()
    self.assertEqual(obj.explicit, start.astimezone(la).date())
    self.assertEqual(obj.implicit, start.astimezone(sydney).date())

def test_trunctime_with_named_tz_and_override_different_current(self):
    """
    Same as above but for TruncTime.
    """
    start = _make_aware(datetime(2023, 6, 1, 12, 5, 30))
    self.create_model(start, start)
    la = pytz.timezone('America/Los_Angeles')
    sydney = pytz.timezone('Australia/Sydney')
    with timezone.override(sydney):
        obj = DTModel.objects.annotate(explicit=TruncTime('start_datetime', tzinfo=la), implicit=TruncTime('start_datetime')).get()
    self.assertEqual(obj.explicit, start.astimezone(la).time())
    self.assertEqual(obj.implicit, start.astimezone(sydney).time())

def test_truncdate_none_returns_none_with_explicit_tzinfo(self):
    """
    TruncDate should return None if the input value is NULL, even when tzinfo
    is provided.
    """
    self.create_model(None, None)
    ny = pytz.timezone('America/New_York')
    self.assertIsNone(DTModel.objects.annotate(truncated=TruncDate('start_datetime', tzinfo=ny)).first().truncated)

def test_trunctime_none_returns_none_with_explicit_tzinfo(self):
    """
    TruncTime should return None for NULL input values when tzinfo is provided.
    """
    self.create_model(None, None)
    ny = pytz.timezone('America/New_York')
    self.assertIsNone(DTModel.objects.annotate(truncated=TruncTime('start_datetime', tzinfo=ny)).first().truncated)
DateFunctionWithTimeZoneTests.test_truncdate_respects_explicit_tzinfo = test_truncdate_respects_explicit_tzinfo
DateFunctionWithTimeZoneTests.test_trunctime_respects_explicit_tzinfo = test_trunctime_respects_explicit_tzinfo
DateFunctionWithTimeZoneTests.test_truncdate_tzinfo_precedence_over_current_timezone = test_truncdate_tzinfo_precedence_over_current_timezone
DateFunctionWithTimeZoneTests.test_trunctime_tzinfo_precedence_over_current_timezone = test_trunctime_tzinfo_precedence_over_current_timezone
DateFunctionWithTimeZoneTests.test_truncdate_with_fixed_offset_tzinfo = test_truncdate_with_fixed_offset_tzinfo
DateFunctionWithTimeZoneTests.test_trunctime_with_fixed_offset_tzinfo = test_trunctime_with_fixed_offset_tzinfo
DateFunctionWithTimeZoneTests.test_truncdate_with_named_tz_and_override_different_current = test_truncdate_with_named_tz_and_override_different_current
DateFunctionWithTimeZoneTests.test_trunctime_with_named_tz_and_override_different_current = test_trunctime_with_named_tz_and_override_different_current
DateFunctionWithTimeZoneTests.test_truncdate_none_returns_none_with_explicit_tzinfo = test_truncdate_none_returns_none_with_explicit_tzinfo
DateFunctionWithTimeZoneTests.test_trunctime_none_returns_none_with_explicit_tzinfo = test_trunctime_none_returns_none_with_explicit_tzinfo