from types import SimpleNamespace
from unittest.mock import patch
from types import SimpleNamespace
from unittest.mock import patch
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransformIsNull, HasKey

class KeyTransformIsNullTests(SimpleTestCase):

    def _make_lhs(self, lhs_sql='COL_SQL', lhs_params=('LHS_PARAM',)):
        """
        Return a mock lhs object with the attributes expected by
        KeyTransformIsNull: .lhs, .key_name and a preprocess_lhs method.
        preprocess_lhs returns (lhs_sql, lhs_params, key_transforms).
        """

        def preprocess_lhs(compiler, connection):
            return (lhs_sql, lhs_params, ['k'])
        return SimpleNamespace(lhs='col', key_name='k', preprocess_lhs=preprocess_lhs)

    def test_oracle_isnull_true_combines_sql_and_params(self):
        lhs = self._make_lhs(lhs_sql='COL_SQL', lhs_params=('LHS_PARAM',))
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='oracle')
        compiler = SimpleNamespace()
        with patch.object(HasKey, 'as_oracle', return_value=('HASKEY_SQL', ('HASP',))) as mock_haskey:
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEY_SQL OR COL_SQL IS NULL)')
            self.assertEqual(params, ('HASP', 'LHS_PARAM'))
            mock_haskey.assert_called_once()

    def test_oracle_isnull_true_with_no_haskey_params_returns_lhs_params_only(self):
        lhs = self._make_lhs(lhs_sql='COL_SQL', lhs_params=('ONLY_LHS',))
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='oracle')
        compiler = SimpleNamespace()
        with patch.object(HasKey, 'as_oracle', return_value=('HASKEY_SQL', ())) as mock_haskey:
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEY_SQL OR COL_SQL IS NULL)')
            self.assertEqual(params, ('ONLY_LHS',))
            mock_haskey.assert_called_once()

    def test_oracle_isnull_true_with_no_params_at_all(self):
        lhs = self._make_lhs(lhs_sql='COL_SQL', lhs_params=())
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='oracle')
        compiler = SimpleNamespace()
        with patch.object(HasKey, 'as_oracle', return_value=('HASKEY_SQL', ())) as mock_haskey:
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEY_SQL OR COL_SQL IS NULL)')
            self.assertEqual(params, ())

    def test_sqlite_isnull_true_uses_is_null_template_and_returns_unmodified_sql(self):
        lhs = self._make_lhs()
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='sqlite')
        compiler = SimpleNamespace()
        captured = {}

        def fake_as_sql(self, compiler_arg, connection_arg, template=None):
            captured['template'] = template
            return ('HAS_SQL', ('HASP',))
        with patch.object(HasKey, 'as_sql', new=fake_as_sql):
            sql, params = lookup.as_sqlite(compiler, connection)
            self.assertEqual(sql, 'HAS_SQL')
            self.assertEqual(params, ('HASP',))
            self.assertEqual(captured['template'], 'JSON_TYPE(%s, %%s) IS NULL')

    def test_sqlite_isnull_true_does_not_negate_sql_and_preserves_params(self):
        lhs = self._make_lhs()
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='sqlite')
        compiler = SimpleNamespace()

        def fake_as_sql(self, compiler_arg, connection_arg, template=None):
            return ('HAS_SQL_MULTI', ('A', 'B'))
        with patch.object(HasKey, 'as_sql', new=fake_as_sql):
            sql, params = lookup.as_sqlite(compiler, connection)
            self.assertEqual(sql, 'HAS_SQL_MULTI')
            self.assertEqual(params, ('A', 'B'))

    def test_oracle_isnull_true_param_order(self):
        """
        Ensure the returned params are the HasKey params followed by the lhs params,
        preserving ordering (HasKey params first).
        """
        lhs = self._make_lhs(lhs_sql='C', lhs_params=('L1', 'L2'))
        lookup = KeyTransformIsNull(lhs, True)
        connection = SimpleNamespace(vendor='oracle')
        compiler = SimpleNamespace()
        with patch.object(HasKey, 'as_oracle', return_value=('HK', ('H1', 'H2'))) as mock_haskey:
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HK OR C IS NULL)')
            self.assertEqual(params, ('H1', 'H2', 'L1', 'L2'))

from unittest import mock
from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransformIsNull, HasKey, KeyTransform

class KeyTransformIsNullTests(SimpleTestCase):

    def setUp(self):
        self.compiler = mock.MagicMock(name='compiler')
        self.connection = mock.MagicMock(name='connection')

    def test_oracle_isnull_true_returns_combined_sql_and_combined_params(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_SQL', ('hp1',))):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS', ('lp1',), ['a'])):
                lookup = KeyTransformIsNull(KeyTransform('a', 'value'), True)
                sql, params = lookup.as_oracle(self.compiler, self.connection)
                self.assertEqual(sql, '(NOT HAS_SQL OR LHS IS NULL)')
                self.assertEqual(params, ('hp1', 'lp1'))

    def test_oracle_param_order_with_multiple_params(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_SQL_MULTI', ('hp1', 'hp2'))):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS', ('lp1', 'lp2'), ['a'])):
                lookup = KeyTransformIsNull(KeyTransform('a', 'value'), True)
                sql, params = lookup.as_oracle(self.compiler, self.connection)
                self.assertEqual(sql, '(NOT HAS_SQL_MULTI OR LHS IS NULL)')
                self.assertEqual(params, ('hp1', 'hp2', 'lp1', 'lp2'))

    def test_sqlite_template_forwarding_includes_params(self):
        with mock.patch.object(HasKey, 'as_sql', return_value=('SQL_FORWARD', ('p1', 'p2'))):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS_FORWARD', ('lp',), ['a'])):
                lookup = KeyTransformIsNull(KeyTransform('a', 'value'), True)
                sql, params = lookup.as_sqlite(self.compiler, self.connection)
                self.assertEqual(sql, 'SQL_FORWARD')
                self.assertEqual(params, ('p1', 'p2'))

    def test_oracle_uses_haskey_result_even_if_haskey_has_no_params(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_NO_PARAMS', ())):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS_NOP', ('lp_only',), ['a'])):
                lookup = KeyTransformIsNull(KeyTransform('a', 'value'), True)
                sql, params = lookup.as_oracle(self.compiler, self.connection)
                self.assertEqual(sql, '(NOT HAS_NO_PARAMS OR LHS_NOP IS NULL)')
                self.assertEqual(params, ('lp_only',))

from types import SimpleNamespace
from unittest import mock
from django.db.models.fields.json import HasKey, KeyTransformIsNull
from django.test import SimpleTestCase

class KeyTransformIsNullLookupTests(SimpleTestCase):

    def test_as_oracle_isnull_true_returns_not_or_haskey_or_lhs_is_null(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', ('lparam',), ['k']))
        lookup = KeyTransformIsNull(lhs, True)
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HKSQL', ('hparam',))):
            sql, params = lookup.as_oracle(None, SimpleNamespace(vendor='oracle'))
        self.assertEqual(sql, '(NOT HKSQL OR COL IS NULL)')
        self.assertEqual(params, ('hparam', 'lparam'))

    def test_as_oracle_isnull_true_param_concatenation_multiple_params(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', ('l1', 'l2'), ['k']))
        lookup = KeyTransformIsNull(lhs, True)
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HKSQL', ('h1', 'h2'))):
            sql, params = lookup.as_oracle(None, SimpleNamespace(vendor='oracle'))
        self.assertEqual(sql, '(NOT HKSQL OR COL IS NULL)')
        self.assertEqual(params, ('h1', 'h2', 'l1', 'l2'))

    def test_as_oracle_isnull_true_with_empty_haskey_params_includes_lhs_params(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', ('lparam',), ['k']))
        lookup = KeyTransformIsNull(lhs, True)
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HKSQL', ())):
            sql, params = lookup.as_oracle(None, SimpleNamespace(vendor='oracle'))
        self.assertEqual(sql, '(NOT HKSQL OR COL IS NULL)')
        self.assertEqual(params, ('lparam',))

    def test_as_oracle_isnull_true_with_no_params_returns_empty_tuple(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', (), ['k']))
        lookup = KeyTransformIsNull(lhs, True)
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HKSQL', ())):
            sql, params = lookup.as_oracle(None, SimpleNamespace(vendor='oracle'))
        self.assertEqual(sql, '(NOT HKSQL OR COL IS NULL)')
        self.assertEqual(params, ())

    def test_as_sqlite_isnull_true_passes_is_null_template_to_haskey(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', ('lparam',), ['k']))
        lookup = KeyTransformIsNull(lhs, True)

        def fake_as_sql(self, compiler, connection, template=None):
            return ('CALLED:' + template, ('hp',))
        with mock.patch.object(HasKey, 'as_sql', new=fake_as_sql):
            sql, params = lookup.as_sqlite(None, SimpleNamespace(vendor='sqlite'))
        expected_template = 'JSON_TYPE(%s, %%s) IS NULL'
        self.assertEqual(sql, 'CALLED:' + expected_template)
        self.assertEqual(params, ('hp',))

    def test_as_sqlite_returns_haskey_as_sql_result_directly(self):
        lhs = SimpleNamespace(lhs='COL', key_name='k', preprocess_lhs=lambda compiler, connection: ('COL', (), ['k']))
        lookup = KeyTransformIsNull(lhs, True)

        def fake_as_sql(self, compiler, connection, template=None):
            return ('SOME_SQL_FOR_TEMPLATE:' + str(template), ())
        with mock.patch.object(HasKey, 'as_sql', new=fake_as_sql):
            sql, params = lookup.as_sqlite(None, SimpleNamespace(vendor='sqlite'))
        self.assertTrue(sql.startswith('SOME_SQL_FOR_TEMPLATE:'))
        self.assertEqual(params, ())

from django.db.models.fields.json import KeyTransform, KeyTransformIsNull, HasKey
from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransform, KeyTransformIsNull, HasKey

class KeyTransformIsNullTests(SimpleTestCase):

    def test_as_oracle_isnull_true_combines_haskey_and_lhs_params(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_KEY_SQL', ('hp',))):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS_SQL', ('lp',), ['k'])):
                lhs = KeyTransform('k', 'value')
                lookup = KeyTransformIsNull(lhs, True)
                sql, params = lookup.as_oracle(compiler=None, connection=None)
                self.assertEqual(sql, '(NOT HAS_KEY_SQL OR LHS_SQL IS NULL)')
                self.assertEqual(params, ('hp', 'lp'))

    def test_as_oracle_isnull_true_concatenates_multiple_params_in_order(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_KEY_SQL', ('hp1', 'hp2'))):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS_SQL', ('lp1', 'lp2'), ['k'])):
                lhs = KeyTransform('k', 'value')
                lookup = KeyTransformIsNull(lhs, True)
                sql, params = lookup.as_oracle(compiler=None, connection=None)
                self.assertEqual(sql, '(NOT HAS_KEY_SQL OR LHS_SQL IS NULL)')
                self.assertEqual(params, ('hp1', 'hp2', 'lp1', 'lp2'))

    def test_as_oracle_preprocess_lhs_called_when_isnull_true(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS', ('p',))):
            preprocess = mock.Mock(return_value=('LHS_SQL', ('lp',), ['k']))
            with mock.patch.object(KeyTransform, 'preprocess_lhs', preprocess):
                lhs = KeyTransform('k', 'value')
                lookup = KeyTransformIsNull(lhs, True)
                lookup.as_oracle(compiler=None, connection=None)
                preprocess.assert_called_once()

    def test_as_oracle_handles_empty_haskey_params(self):
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_KEY_SQL', ())):
            with mock.patch.object(KeyTransform, 'preprocess_lhs', return_value=('LHS_SQL', ('lp',), ['k'])):
                lhs = KeyTransform('k', 'value')
                lookup = KeyTransformIsNull(lhs, True)
                sql, params = lookup.as_oracle(compiler=None, connection=None)
                self.assertEqual(sql, '(NOT HAS_KEY_SQL OR LHS_SQL IS NULL)')
                self.assertEqual(params, ('lp',))

    def test_as_sqlite_calls_haskey_as_sql_once_and_returns_value(self):
        mock_as_sql = mock.Mock(return_value=('SOME_SQL', ('x',)))
        with mock.patch.object(HasKey, 'as_sql', new=mock_as_sql):
            lhs = KeyTransform('k', 'value')
            lookup = KeyTransformIsNull(lhs, True)
            sql, params = lookup.as_sqlite(compiler=None, connection=None)
            mock_as_sql.assert_called_once()
            self.assertEqual(sql, 'SOME_SQL')
            self.assertEqual(params, ('x',))

from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransform, KeyTransformIsNull, HasKey
from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransform, KeyTransformIsNull, HasKey

class KeyTransformIsNullTests(SimpleTestCase):

    def test_oracle_isnull_true_combines_haskey_and_is_null(self):
        compiler = mock.Mock()
        compiler.compile.return_value = ('"value"', ('lhs_param',))
        connection = mock.Mock()
        connection.vendor = 'oracle'

        def fake_haskey_as_oracle(self, compiler_arg, connection_arg):
            return ('HASKEY_SQL', ('hp',))
        with mock.patch.object(HasKey, 'as_oracle', fake_haskey_as_oracle):
            kt = KeyTransform('k', 'value')
            lookup = kt.get_lookup('isnull')(kt, True)
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEY_SQL OR "value" IS NULL)')
            self.assertEqual(params, ('hp', 'lhs_param'))

    def test_oracle_isnull_true_appends_multiple_lhs_params(self):
        compiler = mock.Mock()
        compiler.compile.return_value = ('"value"', ('l1', 'l2'))
        connection = mock.Mock()
        connection.vendor = 'oracle'

        def fake_haskey_as_oracle(self, compiler_arg, connection_arg):
            return ('HASKEY_MULTI', ('hp',))
        with mock.patch.object(HasKey, 'as_oracle', fake_haskey_as_oracle):
            kt = KeyTransform('k', 'value')
            lookup = kt.get_lookup('isnull')(kt, True)
            sql, params = lookup.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEY_MULTI OR "value" IS NULL)')
            self.assertEqual(params, ('hp', 'l1', 'l2'))

from types import SimpleNamespace
from unittest import mock
from types import SimpleNamespace
from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransformIsNull, KeyTransform, HasKey

class KeyTransformIsNullRegressionTests(SimpleTestCase):

    def test_oracle_isnull_true_combines_haskey_sql_and_lhs(self):
        compiler = self._make_compiler(('COLSQL', ('CP',)))
        connection = SimpleNamespace(vendor='oracle')
        with mock.patch.object(HasKey, 'as_oracle', autospec=True, return_value=('HASKEYSQL', ('HP',))) as mocked:
            kt = KeyTransform('mykey', 'colref')
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEYSQL OR COLSQL IS NULL)')
            self.assertEqual(params, ('HP', 'CP'))
            mocked.assert_called_once()

    def test_oracle_isnull_true_haskey_no_params(self):
        compiler = self._make_compiler(('COLSQL', ('CP1', 'CP2')))
        connection = SimpleNamespace(vendor='oracle')
        with mock.patch.object(HasKey, 'as_oracle', autospec=True, return_value=('HASKEYSQL', ())) as mocked:
            kt = KeyTransform('k', 'colref')
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEYSQL OR COLSQL IS NULL)')
            self.assertEqual(params, ('CP1', 'CP2'))
            mocked.assert_called_once()

    def test_oracle_isnull_true_lhs_no_params(self):
        compiler = self._make_compiler(('COLSQL', ()))
        connection = SimpleNamespace(vendor='oracle')
        with mock.patch.object(HasKey, 'as_oracle', autospec=True, return_value=('HASKEYSQL', ('HP', 'HP2'))) as mocked:
            kt = KeyTransform('k', 'colref')
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HASKEYSQL OR COLSQL IS NULL)')
            self.assertEqual(params, ('HP', 'HP2'))
            mocked.assert_called_once()

    def test_oracle_isnull_true_nested_key_transform(self):
        compiler = self._make_compiler(('PREV_COL', ('P1',)))
        connection = SimpleNamespace(vendor='oracle')
        with mock.patch.object(HasKey, 'as_oracle', autospec=True, return_value=('HK', ('H1',))) as mocked:
            kt = KeyTransform('b', KeyTransform('a', 'prev'))
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HK OR PREV_COL IS NULL)')
            self.assertEqual(params, ('H1', 'P1'))
            mocked.assert_called_once()

    def test_sqlite_isnull_true_propagates_multiple_params(self):
        compiler = self._make_compiler(('LHS', ('LP1', 'LP2')))
        connection = SimpleNamespace(vendor='sqlite')

        def side_effect(self_obj, comp, conn, template=None):
            return ('MULTI', ('A', 'B', 'C'))
        with mock.patch.object(HasKey, 'as_sql', autospec=True, side_effect=side_effect):
            kt = KeyTransform('k', 'colref')
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_sqlite(compiler, connection)
            self.assertEqual(sql, 'MULTI')
            self.assertEqual(params, ('A', 'B', 'C'))

    def test_oracle_isnull_true_appends_lhs_params_to_haskey_params(self):
        compiler = self._make_compiler(('LEFT', ('L1', 'L2')))
        connection = SimpleNamespace(vendor='oracle')
        with mock.patch.object(HasKey, 'as_oracle', autospec=True, return_value=('HKSQL', ('H1', 'H2'))) as mocked:
            kt = KeyTransform('z', 'leftcol')
            kisnull = object.__new__(KeyTransformIsNull)
            kisnull.lhs = kt
            kisnull.rhs = True
            sql, params = kisnull.as_oracle(compiler, connection)
            self.assertEqual(sql, '(NOT HKSQL OR LEFT IS NULL)')
            self.assertEqual(params, ('H1', 'H2', 'L1', 'L2'))
            mocked.assert_called_once()

from django.test import TestCase, skipUnlessDBFeature
from django.db import connection
from .models import NullableJSONModel

@skipUnlessDBFeature('supports_json_field')
class KeyTransformIsNullSQLTests(TestCase):

    def test_oracle_isnull_true_includes_or_is_null(self):
        if connection.vendor != 'oracle':
            self.skipTest('Only for Oracle')
        qs = NullableJSONModel.objects.filter(value__a__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_EXISTS', sql.upper())
        self.assertIn('NOT', sql.upper())
        self.assertIn('IS NULL', sql.upper())

    def test_oracle_isnull_false_uses_has_key(self):
        if connection.vendor != 'oracle':
            self.skipTest('Only for Oracle')
        qs = NullableJSONModel.objects.filter(value__a__isnull=False)
        sql = str(qs.query)
        self.assertIn('JSON_EXISTS', sql.upper())
        self.assertNotIn('IS NULL', sql.upper())
        self.assertNotIn('NOT (', sql.upper())

    def test_oracle_nested_isnull_true_includes_or_is_null(self):
        if connection.vendor != 'oracle':
            self.skipTest('Only for Oracle')
        qs = NullableJSONModel.objects.filter(value__baz__a__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_EXISTS', sql.upper())
        self.assertIn('NOT', sql.upper())
        self.assertIn('IS NULL', sql.upper())

    def test_oracle_nested_isnull_false_uses_has_key(self):
        if connection.vendor != 'oracle':
            self.skipTest('Only for Oracle')
        qs = NullableJSONModel.objects.filter(value__baz__a__isnull=False)
        sql = str(qs.query)
        self.assertIn('JSON_EXISTS', sql.upper())
        self.assertNotIn('IS NULL', sql.upper())
        self.assertNotIn('NOT (', sql.upper())

    def test_oracle_array_index_isnull_true_includes_or_is_null(self):
        if connection.vendor != 'oracle':
            self.skipTest('Only for Oracle')
        qs = NullableJSONModel.objects.filter(value__d__0__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_EXISTS', sql.upper())
        self.assertIn('NOT', sql.upper())
        self.assertIn('IS NULL', sql.upper())

    def test_sqlite_isnull_true_uses_json_type_is_null(self):
        if connection.vendor != 'sqlite':
            self.skipTest('Only for SQLite')
        qs = NullableJSONModel.objects.filter(value__a__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_TYPE', sql.upper())
        self.assertIn('IS NULL', sql.upper())
        self.assertNotIn('NOT (', sql.upper())

    def test_sqlite_nested_isnull_true_uses_json_type_is_null(self):
        if connection.vendor != 'sqlite':
            self.skipTest('Only for SQLite')
        qs = NullableJSONModel.objects.filter(value__baz__a__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_TYPE', sql.upper())
        self.assertIn('IS NULL', sql.upper())
        self.assertNotIn('NOT (', sql.upper())

    def test_sqlite_array_index_isnull_true_uses_json_type_is_null(self):
        if connection.vendor != 'sqlite':
            self.skipTest('Only for SQLite')
        qs = NullableJSONModel.objects.filter(value__d__0__isnull=True)
        sql = str(qs.query)
        self.assertIn('JSON_TYPE', sql.upper())
        self.assertIn('IS NULL', sql.upper())
        self.assertNotIn('NOT (', sql.upper())

from unittest import mock
from types import SimpleNamespace
from types import SimpleNamespace
from unittest import mock
from django.test import SimpleTestCase
from django.db.models.fields.json import KeyTransformIsNull, KeyTransform, HasKey, compile_json_path

class KeyTransformIsNullSQLTests(SimpleTestCase):

    def test_oracle_isnull_true_uses_haskey_params_then_lhs_params(self):
        compiler = mock.Mock()
        compiler.compile.return_value = ('"t"."c"', ('LHS_PARAM',))
        conn = SimpleNamespace(vendor='oracle', features=SimpleNamespace())
        with mock.patch.object(HasKey, 'as_oracle', return_value=('HAS_KEY_SQL', ('HP1', 'HP2'))):
            expr = KeyTransformIsNull(KeyTransform('b', 'value'), True)
            sql, params = expr.as_oracle(compiler, conn)
        self.assertEqual(params, ('HP1', 'HP2', 'LHS_PARAM'))
        self.assertIn('IS NULL', sql)
        self.assertIn('HAS_KEY_SQL', sql)

    def test_sqlite_isnull_true_uses_json_type_is_null_and_params(self):
        compiler = mock.Mock()
        compiler.compile.return_value = ('"t"."c"', ('LHS_P',))
        conn = SimpleNamespace(vendor='sqlite', features=SimpleNamespace())
        expr = KeyTransformIsNull(KeyTransform('a', 'value'), True)
        sql, params = expr.as_sqlite(compiler, conn)
        self.assertIn('JSON_TYPE(', sql)
        self.assertIn('IS NULL', sql)
        self.assertTrue(params[0] == 'LHS_P')
        self.assertTrue(any((isinstance(p, str) and p.startswith('$') for p in params[1:])))

    def test_sqlite_integer_key_path_in_isnull_true(self):
        compiler = mock.Mock()
        compiler.compile.return_value = ('col', ('LP',))
        conn = SimpleNamespace(vendor='sqlite', features=SimpleNamespace())
        expr = KeyTransformIsNull(KeyTransform('2', KeyTransform('arr', 'value')), True)
        sql, params = expr.as_sqlite(compiler, conn)
        self.assertIn('[2]', ''.join(params) if any((isinstance(p, str) for p in params)) else str(params))
        self.assertIn('IS NULL', sql)