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

import types
from types import SimpleNamespace
import types
import unittest
from types import SimpleNamespace
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.expressions import OrderBy
from django.db.models.constants import LOOKUP_SEP

def make_compiler(field_is_relation, field_attname, targets, opts_ordering):
    """
    Create an SQLCompiler instance with a stubbed _setup_joins which returns
    the provided fake field, targets, alias/joins, path, opts and transform_function.
    """
    query = DummyQuery()
    compiler = SQLCompiler(query=query, connection=None, using='default')

    def transform_function(target, alias):
        return DummyExpr(f'{target}-{alias}')

    def _setup_joins(self, pieces, opts_param, alias_param):
        field = DummyField(field_is_relation, field_attname)
        joins = ['alias']
        path = None
        return (field, targets, opts_param, joins, path, transform_function)
    compiler._setup_joins = types.MethodType(_setup_joins, compiler)
    opts = SimpleNamespace(ordering=opts_ordering)
    return (compiler, opts)
if __name__ == '__main__':
    unittest.main()

from types import MethodType, SimpleNamespace
from django.db.models.expressions import RawSQL
from types import MethodType, SimpleNamespace
import unittest
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.expressions import RawSQL

def _make_compiler(field_attname, targets, joins=('TJOIN',)):
    """
    Build an SQLCompiler instance with a monkeypatched _setup_joins that
    returns a relation Field (is_relation=True) when the last piece matches
    field_attname, and a non-relation Field otherwise. The transform_function
    returns RawSQL nodes constructed from the targets.
    """
    fake_query = SimpleNamespace()
    fake_query.alias_map = {j: SimpleNamespace(join_cols=('jc',)) for j in joins}
    fake_query.trim_joins = lambda t, j, p: (t, 'ALIA', None)
    compiler = SQLCompiler(fake_query, SimpleNamespace(vendor='sqlite'), using='default')

    def _setup_joins(self, pieces, opts, alias):
        last = pieces[-1]
        if last == field_attname:
            field = SimpleNamespace(is_relation=True, attname=field_attname)
            opts_for_return = SimpleNamespace()
            joins_out = list(joins)
            path = None

            def transform_function(t, alias_inner):
                return RawSQL(str(t), [])
            return (field, list(targets), 'ALIA', joins_out, path, transform_function)
        else:
            field = SimpleNamespace(is_relation=False, attname='nonrel')
            opts_for_return = SimpleNamespace()
            joins_out = list(joins)
            path = None

            def transform_function(t, alias_inner):
                return RawSQL(str(t), [])
            return (field, list(targets), 'ALIA', joins_out, path, transform_function)
    compiler._setup_joins = MethodType(_setup_joins, compiler)
    return compiler

def compile_orderings(compiler, results):
    """
    Compile the OrderBy expressions returned by find_ordering_name into SQL
    strings so we can assert on them. Each result is a tuple (OrderBy, False).
    """
    sqls = []
    for expr, _is_ref in results:
        sql, params = compiler.compile(expr)
        sqls.append(sql)
    return sqls
if __name__ == '__main__':
    unittest.main()

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Author, Article

class OrderingByFKAttnameTests(TestCase):

    def setUp(self):
        self.a1 = Author.objects.create(name='A1')
        self.a2 = Author.objects.create(name='A2')
        now = timezone.now()
        self.art1 = Article.objects.create(author=self.a1, headline='art1', pub_date=now)
        self.art2 = Article.objects.create(author=self.a2, headline='art2', pub_date=now + timedelta(seconds=1))

from django.test import SimpleTestCase
from django.db import connection
import re
from .models import Reference, Article, Author

def _get_sql(qs):
    """
    Helper: compile the queryset's SQL using the default connection.
    Return the SQL string.
    """
    compiler = qs.query.get_compiler(using='default', connection=connection)
    sql, params = compiler.as_sql()
    return sql

def _has_token(sql, token):
    return token in sql

from tests.ordering.models import Author, Article
from django.test import TestCase
import re
from tests.ordering.models import Author, Article
ORDER_BY_RE = re.compile('ORDER BY (.*?)(?:LIMIT|$)', re.IGNORECASE | re.DOTALL)

def _get_order_by_parts(sql):
    """
    Extract a list of ORDER BY items from a SELECT sql string.
    """
    m = ORDER_BY_RE.search(sql)
    if not m:
        return []
    ordering = m.group(1).strip()
    parts = [p.strip() for p in ordering.split(',')]
    return parts