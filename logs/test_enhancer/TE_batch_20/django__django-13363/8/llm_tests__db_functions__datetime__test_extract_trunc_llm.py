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