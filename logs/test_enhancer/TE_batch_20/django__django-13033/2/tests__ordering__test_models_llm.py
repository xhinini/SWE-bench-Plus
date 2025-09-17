from types import MethodType, SimpleNamespace
import unittest
from django.db.models.expressions import OrderBy, RawSQL
from types import MethodType, SimpleNamespace
import unittest
from django.db.models.expressions import OrderBy, RawSQL
from django.db.models.sql.compiler import SQLCompiler

class FindOrderingNameTests(unittest.TestCase):

    def _make_compiler_with_stub(self, field_attname='record_id', targets=('col1',), alias='t0', opts_ordering=None):
        """
        Return an SQLCompiler instance with a stubbed _setup_joins method
        that returns a relation field, targets, alias, joins, path, opts,
        and a transform_function that turns a target name into a RawSQL
        expression referencing alias.target.
        """
        compiler = SQLCompiler(query=None, connection=None, using=None)

        def fake_setup_joins(self, pieces, opts, alias_arg):
            field = SimpleNamespace(is_relation=True, attname=field_attname)
            targets_local = list(targets)
            alias_local = alias
            joins = []
            path = None
            opts_local = opts

            def transform_function(target, alias_inner):
                return RawSQL('%s.%s' % (alias_inner, target), ())
            return (field, targets_local, alias_local, joins, path, opts_local, transform_function)
        compiler._setup_joins = MethodType(fake_setup_joins, compiler)
        compiler.query = SimpleNamespace()
        return compiler

    def test_includes_related_model_ordering_for_record_root_id(self):
        compiler = self._make_compiler_with_stub(field_attname='record_id', targets=('root_id',), alias='r0')
        related_order = OrderBy(RawSQL('related_table.some_col', ()), descending=True)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('record__root_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order, returned_exprs)

    def test_includes_related_model_ordering_for_complex_lookup_ending_with_id(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_id', targets=('c1', 'c2'), alias='a1')
        related_order = OrderBy(RawSQL('related_table.x', ()), descending=False)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('a__b__c_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order, returned_exprs)
        self.assertTrue(any((isinstance(r[0], OrderBy) for r in result)))

    def test_preserves_related_ordering_when_name_has_leading_minus_and_endswith_id(self):
        compiler = self._make_compiler_with_stub(field_attname='record_id', targets=('root_id',), alias='r2')
        related_order = OrderBy(RawSQL('related_table.z', ()), descending=False)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('-record__root_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order, returned_exprs)

    def test_includes_related_ordering_when_attname_differs_from_last_piece_and_endswith_id(self):
        compiler = self._make_compiler_with_stub(field_attname='different_attname', targets=('root_id',), alias='a3')
        related_order = OrderBy(RawSQL('rt.blah', ()), descending=True)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('some__root_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order, returned_exprs)

    def test_multiple_related_ordering_entries_appended_for_id_suffix(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_id', targets=('t1',), alias='aliasX')
        related_order1 = OrderBy(RawSQL('r.a', ()), descending=False)
        related_order2 = OrderBy(RawSQL('r.b', ()), descending=True)
        opts = SimpleNamespace(ordering=[related_order1, related_order2])
        result = compiler.find_ordering_name('x__y__z_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order1, returned_exprs)
        self.assertIn(related_order2, returned_exprs)

    def test_related_ordering_appended_for_many_targets_when_lookup_endswith_id(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_field_id', targets=('a', 'b', 'c'), alias='ALIAS')
        related_order = OrderBy(RawSQL('other.x', ()), descending=False)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('one__two__three_id', opts)
        returned_exprs = [r[0] for r in result]
        self.assertIn(related_order, returned_exprs)
        self.assertGreaterEqual(len(result), 1)

    def test_related_ordering_appended_when_ordering_is_orderby_instance(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_id', targets=('c',), alias='A0')
        related_order = OrderBy(RawSQL('tbl.col', ()), descending=True)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('m__n_id', opts)
        self.assertIn(related_order, [r[0] for r in result])

    def test_related_ordering_appended_with_mixed_case_name_ending_with_id(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_id', targets=('t',), alias='XYZ')
        related_order = OrderBy(RawSQL('R.C', ()), descending=False)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('Some__Very__long_id', opts)
        self.assertIn(related_order, [r[0] for r in result])

    def test_related_ordering_appended_for_deep_lookup_ending_with_id(self):
        compiler = self._make_compiler_with_stub(field_attname='fk_id', targets=('deepcol',), alias='deep_alias')
        related_order = OrderBy(RawSQL('deep.tbl', ()), descending=True)
        opts = self._make_opts_with_ordering(related_order)
        result = compiler.find_ordering_name('a__b__c__d__deep_id', opts)
        self.assertIn(related_order, [r[0] for r in result])
if __name__ == '__main__':
    unittest.main()