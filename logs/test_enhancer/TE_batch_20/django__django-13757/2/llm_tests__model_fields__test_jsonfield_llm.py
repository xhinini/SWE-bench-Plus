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