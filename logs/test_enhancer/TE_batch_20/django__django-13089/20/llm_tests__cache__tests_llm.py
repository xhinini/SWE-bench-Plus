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

from django.core import management
from django.db import connection
from django.core.cache import caches
from django.test import TransactionTestCase, override_settings
from django.conf import settings
import time
try:
    from .tests import caches_setting_for_tests
except Exception:

    def caches_setting_for_tests(**params):
        base = {}
        setting = {'default': base}
        setting['default'].update(params)
        return setting

@override_settings(CACHES=caches_setting_for_tests(BACKEND='django.core.cache.backends.db.DatabaseCache', LOCATION='test cache table cull_none', OPTIONS={'MAX_ENTRIES': 0, 'CULL_FREQUENCY': 100}))
class DatabaseCacheCullFetchoneNoneTests(TransactionTestCase):
    """
    Tests that exercise the _cull() path where the culling-selection SQL
    returns no rows (cursor.fetchone() is None). In the buggy implementation,
    that led to indexing into None and an exception.
    """
    available_apps = ['cache']

    def setUp(self):
        super().setUp()
        management.call_command('createcachetable', verbosity=0)

from unittest import mock
from django.core.cache import caches
from django.db import router, connections
from django.utils import timezone

def _attach_tests(DBCacheTests):

    def test_cull_handles_missing_last_cache_key_no_exception(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), None])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key <'))

    def test_cull_deletes_when_last_cache_key_present(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), ('last-key',)])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertTrue(self._calls_sql_containing(mock_cursor, 'cache_key <'))
        found = False
        for call in mock_cursor.execute.call_args_list:
            args, kwargs = call
            if args and 'cache_key <' in args[0]:
                params = args[1] if len(args) > 1 else []
                if params and params[0] == 'last-key':
                    found = True
        self.assertTrue(found, "Expected delete-by-key call with 'last-key' parameter")

    def test_cull_ignores_none_tuple_element(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), (None,)])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key <'))

    def test_cull_ignores_empty_sequence(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), []])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key <'))

    def test_cull_calls_culling_sql_with_correct_cull_num(self):
        cull_cache, db = self._get_cull_cache_and_db()
        old_freq = cull_cache._cull_frequency
        cull_cache._cull_frequency = 4
        try:
            mock_cursor = mock.Mock()
            mock_cursor.fetchone = mock.Mock(side_effect=[(101,), ('last',)])
            mock_cursor.execute = mock.Mock()
            now = timezone.now().replace(microsecond=0)
            cull_cache._cull(db, mock_cursor, now)
            found = False
            for call in mock_cursor.execute.call_args_list:
                args, kwargs = call
                if len(args) > 1 and args[1] == [101 // 4]:
                    found = True
            self.assertTrue(found, 'Expected culling SQL to be executed with cull_num == 101 // 4')
        finally:
            cull_cache._cull_frequency = old_freq

    def test_cull_skips_when_under_max_entries(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(10,)])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key_culling_sql') or self._calls_sql_containing(mock_cursor, 'cache_key <'))

    def test_cull_handles_empty_tuple(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(31,), tuple()])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key <'))

    def test_cull_handles_bytes_last_cache_key(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), (b'keybytes',)])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        found = False
        for call in mock_cursor.execute.call_args_list:
            args, kwargs = call
            if args and 'cache_key <' in args[0]:
                params = args[1] if len(args) > 1 else []
                if params and params[0] == b'keybytes':
                    found = True
        self.assertTrue(found)

    def test_zero_cull_calls_clear(self):
        zero_cull_cache = caches['zero_cull']
        db = router.db_for_write(zero_cull_cache.cache_model_class)
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), None])
        mock_cursor.execute = mock.Mock()
        with mock.patch.object(zero_cull_cache, 'clear', autospec=True) as mock_clear:
            now = timezone.now().replace(microsecond=0)
            zero_cull_cache._cull(db, mock_cursor, now)
            mock_clear.assert_called_once()

    def test_cull_ignores_last_cache_key_with_empty_string(self):
        cull_cache, db = self._get_cull_cache_and_db()
        mock_cursor = mock.Mock()
        mock_cursor.fetchone = mock.Mock(side_effect=[(100,), ('',)])
        mock_cursor.execute = mock.Mock()
        now = timezone.now().replace(microsecond=0)
        cull_cache._cull(db, mock_cursor, now)
        self.assertFalse(self._calls_sql_containing(mock_cursor, 'cache_key <'))
    test_methods = [test_cull_handles_missing_last_cache_key_no_exception, test_cull_deletes_when_last_cache_key_present, test_cull_ignores_none_tuple_element, test_cull_ignores_empty_sequence, test_cull_calls_culling_sql_with_correct_cull_num, test_cull_skips_when_under_max_entries, test_cull_handles_empty_tuple, test_cull_handles_bytes_last_cache_key, test_zero_cull_calls_clear, test_cull_ignores_last_cache_key_with_empty_string]
    for func in test_methods:
        setattr(DBCacheTests, func.__name__, func)
try:
    from django.core.cache.tests import DBCacheTests as _DBCacheTests_module
except Exception:
    from tests.cache.tests import DBCacheTests as _DBCacheTests_module
_attach_tests(_DBCacheTests_module)

from contextlib import contextmanager
from django.core import management
from django.db import connections, router
from django.test import TransactionTestCase, override_settings
from contextlib import contextmanager
import time
from datetime import datetime, timedelta
from django.core import management
from django.conf import settings
from django.core.cache import cache, caches
from django.db import connections, router
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from django.core.cache.backends.db import DatabaseCache
CACHE_TABLE_NAME = 'test cache table'
CACHES_OVERRIDE = {'default': {'BACKEND': 'django.core.cache.backends.db.DatabaseCache', 'LOCATION': CACHE_TABLE_NAME}}

@override_settings(CACHES=CACHES_OVERRIDE)
class CullRegressionTests(TransactionTestCase):
    available_apps = ['cache']

    def setUp(self):
        super().setUp()
        management.call_command('createcachetable', verbosity=0)
        self.cache = caches['default']

    def _count_table_rows(self):
        db = router.db_for_read(self.cache.cache_model_class)
        conn = connections[db]
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM %s' % conn.ops.quote_name(CACHE_TABLE_NAME))
            return cursor.fetchone()[0]

from unittest import mock
from django.core.cache.backends.db import DatabaseCache
from django.db import router, connections
from django.utils import timezone
from unittest import mock
from django.test import SimpleTestCase
from django.core.cache.backends.db import DatabaseCache
from django.db import router, connections
from django.utils import timezone

class DBCacheCullingTests(SimpleTestCase):

    def setUp(self):
        self.cache = DatabaseCache('test cache table', {'TIMEOUT': 300})
        self.cache._max_entries = 10
        self.cache._cull_frequency = 3

    def _get_db(self):
        return router.db_for_write(self.cache.cache_model_class)

from django.core import management
from django.core.cache import caches
from django.db import connections, router
from django.conf import settings
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from django.db import connection
import time

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.db.DatabaseCache', 'LOCATION': 'test cache table'}})
class DatabaseCacheCullingRegressionTests(TransactionTestCase):
    available_apps = ['cache']

    def setUp(self):
        super().setUp()
        management.call_command('createcachetable', verbosity=0)
        self.cache = caches['default']
        self.now = timezone.now().replace(microsecond=0)

    def _table_count(self):
        with connection.cursor() as cursor:
            table_name = connection.ops.quote_name('test cache table')
            cursor.execute('SELECT COUNT(*) FROM %s' % table_name)
            return cursor.fetchone()[0]

from django.core import management
from django.db import connection, connections
from django.test import TransactionTestCase, override_settings
from django.core.cache import caches
from cache.tests import caches_setting_for_tests
from django.core import management
from django.db import connection, connections
from django.test import TransactionTestCase, override_settings
from django.core.cache import caches
from django.conf import settings
import time
from cache.tests import caches_setting_for_tests

@override_settings(CACHES=caches_setting_for_tests(BACKEND='django.core.cache.backends.db.DatabaseCache', LOCATION='test cache table'))
class AdditionalDBCullTests(TransactionTestCase):
    available_apps = ['cache']

    def setUp(self):
        super().setUp()
        management.call_command('createcachetable', verbosity=0)
        self.cache = caches['default']
        self.conn = connections[self._db_for_cache()]
        self.quoted_table = self.conn.ops.quote_name('test cache table')

    def _db_for_cache(self):
        return 'default'

    def _row_count(self):
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM %s' % self.quoted_table)
            return cursor.fetchone()[0]

from unittest import mock
from django.core.cache import caches
from django.utils import timezone

def test__cull_handles_none_last_cache_key_no_delete(self):
    """
    If the cache_key_culling_sql() query doesn't return a last cache key
    (cursor.fetchone() is None), _cull() must not attempt to subscript None
    and should not execute the final DELETE ... WHERE cache_key < ... query.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(100,), None]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    executed_sqls = [call_args[0][0] for call_args in m_cursor.execute.call_args_list]
    assert not any(('WHERE cache_key <' in sql for sql in executed_sqls)), "Expected no 'WHERE cache_key <' delete to be executed when cursor.fetchone() returned None for last cache key."

def test__cull_deletes_when_last_cache_key_present(self):
    """
    When a last cache key is returned by cache_key_culling_sql(), _cull()
    should execute a DELETE ... WHERE cache_key < <last_key> query with the
    last key passed as a parameter.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(100,), ('last-cache-key',)]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    for args, kwargs in m_cursor.execute.call_args_list:
        sql = args[0]
        if 'WHERE cache_key <' in sql:
            params = args[1]
            assert params == ['last-cache-key'], 'DELETE should be executed with the last cache key as parameter.'
            break
    else:
        raise AssertionError('Expected a delete-by-cache-key SQL to be executed.')

def test__cull_no_culling_if_count_not_exceeding_max_entries(self):
    """
    If the rowcount returned by SELECT COUNT(*) is not greater than
    _max_entries, _cull() should not call the cache_key_culling_sql() path.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(1,)]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    executed_sqls = [call_args[0][0] for call_args in m_cursor.execute.call_args_list]
    assert not any(('cache_key_culling' in sql or 'WHERE cache_key <' in sql for sql in executed_sqls))

def test__cull_calls_clear_when_cull_frequency_zero(self):
    """
    If _cull_frequency is 0, _cull() should call clear() instead of trying
    to perform culling.
    """
    cache_obj = caches['cull']
    old_frequency = cache_obj._cull_frequency
    try:
        cache_obj._cull_frequency = 0
        cache_obj.clear = mock.MagicMock()
        now = timezone.now()
        m_cursor = mock.MagicMock()
        m_cursor.fetchone.return_value = (0,)
        cache_obj._cull('default', m_cursor, now)
        assert cache_obj.clear.called, 'clear() should be called when _cull_frequency == 0'
    finally:
        cache_obj._cull_frequency = old_frequency

def test__cull_passes_computed_cull_num_to_culling_sql(self):
    """
    Ensure the cull_num (num // _cull_frequency) is passed as the parameter
    to the cache_key_culling_sql() execute call.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    num = 100
    old_cull_freq = cache_obj._cull_frequency
    try:
        cache_obj._cull_frequency = 4
        m_cursor.fetchone.side_effect = [(num,), ('lastkey',)]
        m_cursor.execute = mock.MagicMock()
        cache_obj._cull('default', m_cursor, now)
        found = False
        expected_cull_num = num // cache_obj._cull_frequency
        for args, kwargs in m_cursor.execute.call_args_list:
            if len(args) >= 2 and isinstance(args[1], (list, tuple)) and (args[1] == [expected_cull_num]):
                found = True
                break
        assert found, 'cull_num was not passed correctly to the culling SQL execute() call.'
    finally:
        cache_obj._cull_frequency = old_cull_freq

def test__cull_handles_last_cache_key_with_none_element(self):
    """
    If cursor.fetchone() returns a tuple where the first element is None
    (e.g. (None,)), _cull() should still attempt the delete (the tuple is
    truthy) and pass None as the parameter. This verifies handling of
    truthy-but-empty values and ensures no TypeError is raised.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(100,), (None,)]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    for args, kwargs in m_cursor.execute.call_args_list:
        sql = args[0]
        if 'WHERE cache_key <' in sql:
            params = args[1]
            assert params == [None], 'Expected the delete to be called with [None] as parameter.'
            break
    else:
        raise AssertionError('Expected a delete-by-cache-key SQL to be executed.')

def test__cull_handles_last_cache_key_as_bytes(self):
    """
    If the last cache key returned is bytes, the code should use it as-is
    and pass it to the delete query as the parameter.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(100,), (b'byte-key',)]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    for args, kwargs in m_cursor.execute.call_args_list:
        sql = args[0]
        if 'WHERE cache_key <' in sql:
            params = args[1]
            assert params == [b'byte-key'], 'Expected the delete to be called with the bytes key as parameter.'
            break
    else:
        raise AssertionError('Expected a delete-by-cache-key SQL to be executed.')

def test__cull_no_exception_when_cull_num_is_zero_and_no_last_key(self):
    """
    If the cull_num computes to zero (num // _cull_frequency == 0) but the
    cache_key_culling_sql() still runs and fetchone() returns None, _cull()
    must not raise.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    old_cull_freq = cache_obj._cull_frequency
    try:
        cache_obj._cull_frequency = 99999
        m_cursor.fetchone.side_effect = [(1000,), None]
        m_cursor.execute = mock.MagicMock()
        cache_obj._cull('default', m_cursor, now)
    finally:
        cache_obj._cull_frequency = old_cull_freq

def test__cull_multiple_execute_calls_observed(self):
    """
    Ensure that when last_cache_key is present, _cull() performs the sequence
    of SQL execution calls including the culling SQL and the subsequent
    delete-by-cache-key. This is a sanity check that validates the expected
    call ordering.
    """
    cache_obj = caches['cull']
    now = timezone.now()
    m_cursor = mock.MagicMock()
    m_cursor.fetchone.side_effect = [(200,), ('last-key',)]
    m_cursor.execute = mock.MagicMock()
    cache_obj._cull('default', m_cursor, now)
    assert len(m_cursor.execute.call_args_list) >= 3, 'Expected multiple execute() calls during culling.'