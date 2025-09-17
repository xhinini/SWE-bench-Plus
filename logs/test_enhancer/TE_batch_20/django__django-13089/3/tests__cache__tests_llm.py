import types
from django.db import connections
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.test import override_settings

def _get_table_for_default_cache():
    db = cache._router.db_for_write(cache.cache_model_class)
    connection = connections[db]
    return (connection.ops.quote_name(cache._table), connection)

def test_cull_handles_none_last_cache_key_no_exception():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), None])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 3
    cache._cull(connection.alias, fake_cursor, now)

def test_cull_does_not_execute_delete_when_no_last_cache_key():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), None])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 3
    cache._cull(connection.alias, fake_cursor, now)
    assert len(fake_cursor.calls) == 3, 'Unexpected DELETE executed when no last_cache_key was returned'

def test_cull_executes_delete_when_last_cache_key_present():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), ('last-key',)])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 3
    cache._cull(connection.alias, fake_cursor, now)
    assert len(fake_cursor.calls) == 4, 'Expected a DELETE to be executed when last_cache_key is present'
    last_sql = fake_cursor.calls[-1][0]
    assert 'DELETE' in last_sql and 'cache_key <' in last_sql, 'Last executed SQL was not the expected culling DELETE'

def test_cull_skips_culling_when_num_below_max_entries():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(2,)])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 3
    cache._cull(connection.alias, fake_cursor, now)
    assert len(fake_cursor.calls) == 2, 'Unexpected culling when count is below max_entries'

def test_cull_calls_clear_when_cull_frequency_zero(monkeypatch):
    called = {'clear': False}

    def fake_clear():
        called['clear'] = True
    monkeypatch.setattr(cache, 'clear', fake_clear)
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), ('will-not-be-used',)])
    now = timezone.now()
    cache._max_entries = -1
    cache._cull_frequency = 0
    cache._cull(connection.alias, fake_cursor, now)
    assert called['clear'] is True, 'clear() was not called when _cull_frequency == 0'

def test_cull_multiple_times_with_none_last_key():
    table, connection = _get_table_for_default_cache()
    for _ in range(3):
        fake_cursor = FakeCursor([(10,), None])
        now = timezone.now()
        cache._max_entries = 5
        cache._cull_frequency = 3
        cache._cull(connection.alias, fake_cursor, now)

def test_cull_with_empty_string_key_performs_delete():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), ('',)])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 3
    cache._cull(connection.alias, fake_cursor, now)
    assert len(fake_cursor.calls) == 4, 'Expected DELETE to be executed even with empty string last key'

def test_cull_none_last_key_when_adapter_used():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(10,), None])
    now = timezone.now()
    cache._max_entries = 1
    cache._cull_frequency = 2
    cache._cull(connection.alias, fake_cursor, now)

def test_cull_executes_culling_sql_with_cull_num_and_handles_no_result():
    table, connection = _get_table_for_default_cache()
    fake_cursor = FakeCursor([(20,), None])
    now = timezone.now()
    cache._max_entries = 5
    cache._cull_frequency = 4
    cache._cull(connection.alias, fake_cursor, now)
    assert len(fake_cursor.calls) >= 3, 'Expected at least 3 execute calls'
    culling_call = fake_cursor.calls[2]
    cull_params = culling_call[1]
    assert isinstance(cull_params, list) and len(cull_params) == 1 and isinstance(cull_params[0], int), 'cull_num parameter missing or invalid'

def test_repeated_cull_varied_counts():
    table, connection = _get_table_for_default_cache()
    now = timezone.now()
    for count, expected_execs in ((1, 2), (6, 3), (100, 3)):
        fake_cursor = FakeCursor([(count,), None])
        cache._max_entries = 5
        cache._cull_frequency = 3
        cache._cull(connection.alias, fake_cursor, now)
        assert len(fake_cursor.calls) >= expected_execs, 'Unexpected number of SQL executes for count=%r' % (count,)
globals().update({'test_cull_handles_none_last_cache_key_no_exception': test_cull_handles_none_last_cache_key_no_exception, 'test_cull_does_not_execute_delete_when_no_last_cache_key': test_cull_does_not_execute_delete_when_no_last_cache_key, 'test_cull_executes_delete_when_last_cache_key_present': test_cull_executes_delete_when_last_cache_key_present, 'test_cull_skips_culling_when_num_below_max_entries': test_cull_skips_culling_when_num_below_max_entries, 'test_cull_calls_clear_when_cull_frequency_zero': test_cull_calls_clear_when_cull_frequency_zero, 'test_cull_multiple_times_with_none_last_key': test_cull_multiple_times_with_none_last_key, 'test_cull_with_empty_string_key_performs_delete': test_cull_with_empty_string_key_performs_delete, 'test_cull_none_last_key_when_adapter_used': test_cull_none_last_key_when_adapter_used, 'test_cull_executes_culling_sql_with_cull_num_and_handles_no_result': test_cull_executes_culling_sql_with_cull_num_and_handles_no_result, 'test_repeated_cull_varied_counts': test_repeated_cull_varied_counts})

from django.core.cache.backends.db import DatabaseCache
from django.utils import timezone
from django.db import connections
from unittest import mock
from django.test import SimpleTestCase
from django.core.cache.backends.db import DatabaseCache
from django.utils import timezone
from django.db import connections
from unittest import mock
from django.test import SimpleTestCase

class DatabaseCacheCullTests(SimpleTestCase):

    def make_connection(self, quote_name_func=None, adapt_func=None, culling_sql=None):
        """
        Helper to make a fake connection with ops that provide quote_name,
        adapt_datetimefield_value and cache_key_culling_sql.
        """
        conn = mock.Mock()
        ops = mock.Mock()
        ops.quote_name.side_effect = lambda x: quote_name_func(x) if quote_name_func else x
        ops.adapt_datetimefield_value.side_effect = lambda x: adapt_func(x) if adapt_func else x
        ops.cache_key_culling_sql.return_value = culling_sql or 'SELECT cache_key FROM %s ORDER BY cache_key LIMIT %s'
        conn.ops = ops
        return conn