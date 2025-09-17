from django.db.models.expressions import SimpleCol, F
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from .models import Item

class TestResolveLookupValueNestedIterables(SimpleTestCase):

    def test_resolve_lookup_value_nested_list_resolves_inner_F(self):
        q = Query(Item)
        value = [[F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_nested_tuple_resolves_inner_F(self):
        q = Query(Item)
        value = ((F('created'),),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_list_with_tuple_inner_preserves_inner_type(self):
        q = Query(Item)
        value = [(F('created'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_tuple_with_list_inner_preserves_inner_type(self):
        q = Query(Item)
        value = ([F('created')],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_mixed_nested_iterables(self):
        q = Query(Item)
        value = [F('created'), [F('modified'), F('created')], (F('created'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], SimpleCol)
        self.assertEqual(resolved[0].target, Item._meta.get_field('created'))
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertIsInstance(resolved[1][1], SimpleCol)
        self.assertIsInstance(resolved[2], tuple)
        self.assertIsInstance(resolved[2][0], SimpleCol)

    def test_resolve_lookup_value_deeply_nested_three_levels(self):
        q = Query(Item)
        value = [[[F('created')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)
        self.assertEqual(resolved[0][0][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_deeply_nested_mixed_types(self):
        q = Query(Item)
        value = ([([F('created')],)],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        inner_list = resolved[0]
        self.assertIsInstance(inner_list, list)
        inner_tuple = inner_list[0]
        self.assertIsInstance(inner_tuple, tuple)
        inner_most_list = inner_tuple[0]
        self.assertIsInstance(inner_most_list, list)
        self.assertIsInstance(inner_most_list[0], SimpleCol)
        self.assertEqual(inner_most_list[0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_multiple_levels_with_non_expressions(self):
        q = Query(Item)
        value = ([F('created'), 'x'], ('y', [F('modified')]))
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[1], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(resolved[0][1], 'x')
        self.assertEqual(resolved[1][0], 'y')
        self.assertIsInstance(resolved[1][1], list)
        self.assertIsInstance(resolved[1][1][0], SimpleCol)
        self.assertEqual(resolved[1][1][0].target, Item._meta.get_field('modified'))

from django.db.models import F
from django.test import SimpleTestCase
from django.db.models.sql.query import Query
from .models import Item

class TestResolveLookupValueNested(SimpleTestCase):

    def test_nested_list_resolves_F(self):
        q = Query(Item)
        value = [[F('id')]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertFalse(self._contains_F(res))

    def test_nested_tuple_resolves_F(self):
        q = Query(Item)
        value = ((F('id'),),)
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], tuple)
        self.assertFalse(self._contains_F(res))

    def test_deeply_nested_mixed_resolves_all_F(self):
        q = Query(Item)
        value = [(F('id'), [F('name'), (F('created'),)]), F('id')]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertFalse(self._contains_F(res))

    def test_multiple_elements_mixed_depth(self):
        q = Query(Item)
        value = [F('id'), [F('name')], (F('created'),)]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertFalse(self._contains_F(res))

    def test_nested_list_preserves_inner_types(self):
        q = Query(Item)
        value = [(F('id'),), [F('name')]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[1], list)
        self.assertFalse(self._contains_F(res))

    def test_nested_tuple_preserves_inner_types(self):
        q = Query(Item)
        value = ([F('name')], (F('id'),))
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[1], tuple)
        self.assertFalse(self._contains_F(res))

    def test_mixed_deep_nesting_all_resolved(self):
        q = Query(Item)
        value = ([(F('id'), [(F('name'),), []])],)
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertFalse(self._contains_F(res))

from django.db.models.expressions import BaseExpression
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item
from django.test import SimpleTestCase
from django.db.models.expressions import BaseExpression
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item

class ResolveLookupValueTests(SimpleTestCase):

    def setUp(self):
        self.query = Query(Item)

    def test_nested_list_resolves_inner_expressions(self):
        nested = [['a', F('id')]]
        res = self.query.resolve_lookup_value(nested, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][1], BaseExpression)
        self.assertNotIsInstance(res[0][1], F)

    def test_nested_tuple_resolves_inner_expressions_and_preserves_types(self):
        nested = ((F('id'),),)
        res = self.query.resolve_lookup_value(nested, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][0], BaseExpression)
        self.assertNotIsInstance(res[0][0], F)

    def test_mixed_nested_types_resolve_all_expressions(self):
        mixed = [(F('id'), ['x', F('id')])]
        res = self.query.resolve_lookup_value(mixed, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][1], list)
        self.assertIsInstance(res[0][0], BaseExpression)
        self.assertNotIsInstance(res[0][0], F)
        self.assertIsInstance(res[0][1][1], BaseExpression)
        self.assertNotIsInstance(res[0][1][1], F)

    def test_deeply_nested_resolves(self):
        deep = [[[F('id')]]]
        res = self.query.resolve_lookup_value(deep, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], list)
        self.assertIsInstance(res[0][0][0], BaseExpression)
        self.assertNotIsInstance(res[0][0][0], F)

    def test_multiple_expressions_in_inner_iterable_are_all_resolved(self):
        val = [[F('id'), F('id'), 'x']]
        res = self.query.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        inner = res[0]
        self.assertIsInstance(inner[0], BaseExpression)
        self.assertIsInstance(inner[1], BaseExpression)
        self.assertEqual(inner[2], 'x')

    def test_preserve_and_resolve_mixed_sequence_types(self):
        val = (['start', (F('id'),)],)
        res = self.query.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][1], tuple)
        self.assertIsInstance(res[0][1][0], BaseExpression)
        self.assertNotIsInstance(res[0][1][0], F)

from django.db.models.expressions import Col, SimpleCol, BaseExpression
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Author
from django.test import SimpleTestCase

class TestResolveLookupValueNested(SimpleTestCase):

    def test_nested_list_resolves_F_to_col(self):
        q = Query(Author)
        value = [[F('id')]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], (Col, SimpleCol))
        self.assertNotIsInstance(res[0][0], F)

    def test_nested_tuple_resolves_F_to_col(self):
        q = Query(Author)
        value = ((F('id'),),)
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][0], (Col, SimpleCol))
        self.assertNotIsInstance(res[0][0], F)

    def test_deeply_nested_resolves_F(self):
        q = Query(Author)
        value = [[[(F('id'),)]]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], list)
        self.assertIsInstance(res[0][0][0], tuple)
        self.assertIsInstance(res[0][0][0][0], (Col, SimpleCol))
        self.assertNotIsInstance(res[0][0][0][0], F)

    def test_mixed_list_tuple_preserves_types_and_resolves(self):
        q = Query(Author)
        value = ([F('id'), 'x'], ('y', F('num')))
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[1], tuple)
        self.assertIsInstance(res[0][0], (Col, SimpleCol))
        self.assertEqual(res[0][1], 'x')
        self.assertEqual(res[1][0], 'y')
        self.assertIsInstance(res[1][1], (Col, SimpleCol))

    def test_non_expression_items_unchanged_inside_nested(self):
        q = Query(Author)
        value = [['a', 1, F('id')]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertEqual(res[0][0], 'a')
        self.assertEqual(res[0][1], 1)
        self.assertIsInstance(res[0][2], (Col, SimpleCol))

    def test_nested_multiple_Fs_resolved(self):
        q = Query(Author)
        value = [[F('id'), F('num')]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res[0][0], (Col, SimpleCol))
        self.assertIsInstance(res[0][1], (Col, SimpleCol))

    def test_nested_structures_with_multiple_levels_and_types(self):
        q = Query(Author)
        value = (['a', (F('id'),)], [['b', F('num')], ()])
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][1], tuple)
        self.assertIsInstance(res[0][1][0], (Col, SimpleCol))
        self.assertIsInstance(res[1], list)
        self.assertIsInstance(res[1][0], list)
        self.assertIsInstance(res[1][0][1], (Col, SimpleCol))

from django.test import SimpleTestCase
from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item

class TestQueryNestedResolve(SimpleTestCase):

    def test_nested_list_of_f_resolves(self):
        q = Query(Item)
        value = [[F('id')]]
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], list)
        self.assertEqual(len(res[0]), 1)
        self.assertIsInstance(res[0][0], SimpleCol)

    def test_nested_tuple_of_f_resolves_and_preserves_type(self):
        q = Query(Item)
        value = ((F('id'),),)
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], tuple)
        self.assertEqual(len(res[0]), 1)
        self.assertIsInstance(res[0][0], SimpleCol)

    def test_mixed_list_and_tuple_nested_resolves(self):
        q = Query(Item)
        value = [(F('id'), [F('created')])]
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)
        inner = res[0]
        self.assertIsInstance(inner, tuple)
        self.assertIsInstance(inner[0], SimpleCol)
        self.assertIsInstance(inner[1], list)
        self.assertIsInstance(inner[1][0], SimpleCol)

    def test_deeply_nested_three_levels(self):
        q = Query(Item)
        value = [[[[F('id')]]]]
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], list)
        self.assertIsInstance(res[0][0][0], list)
        self.assertIsInstance(res[0][0][0][0], SimpleCol)

    def test_nested_mixed_values_and_f(self):
        q = Query(Item)
        value = ['a', (F('id'),), ['b', F('created')]]
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, list)
        self.assertEqual(res[0], 'a')
        self.assertIsInstance(res[1], tuple)
        self.assertIsInstance(res[1][0], SimpleCol)
        self.assertIsInstance(res[2], list)
        self.assertEqual(res[2][0], 'b')
        self.assertIsInstance(res[2][1], SimpleCol)

    def test_nested_tuple_of_lists_of_tuples(self):
        q = Query(Item)
        value = ([(F('id'),)],)
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], tuple)
        self.assertIsInstance(res[0][0][0], SimpleCol)

from django.test import SimpleTestCase
from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item

class TestResolveLookupValueNested(SimpleTestCase):

    def test_nested_list_of_f(self):
        q = Query(Item)
        value = [[F('created')]]
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_nested_tuple_of_f(self):
        q = Query(Item)
        value = ((F('created'),),)
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_mixed_inner_types(self):
        q = Query(Item)
        value = [(F('created'),), [F('modified')]]
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[1], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(result[1][0].target, Item._meta.get_field('modified'))

    def test_deeply_nested_lists(self):
        q = Query(Item)
        value = [[[F('created')]]]
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], list)
        self.assertIsInstance(result[0][0][0], SimpleCol)
        self.assertEqual(result[0][0][0].target, Item._meta.get_field('created'))

    def test_nested_with_nonexprs_preserved(self):
        q = Query(Item)
        value = [[1, F('created'), 'x']]
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[0][2], 'x')
        self.assertIsInstance(result[0][1], SimpleCol)
        self.assertEqual(result[0][1].target, Item._meta.get_field('created'))

    def test_preserve_inner_tuple_type(self):
        q = Query(Item)
        value = [(F('created'),)]
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_multiple_exprs_in_nested_structure(self):
        q = Query(Item)
        value = ((F('created'),), [F('modified'), F('created')])
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[1], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertIsInstance(result[1][1], SimpleCol)

    def test_nested_mixed_depth_and_types(self):
        q = Query(Item)
        value = ([(F('created'),), []],)
        result = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], tuple)
        self.assertIsInstance(result[0][0][0], SimpleCol)
        self.assertEqual(result[0][0][0].target, Item._meta.get_field('created'))

from django.db.models.expressions import SimpleCol, F
from django.db.models.sql.query import Query
from .models import Item
from django.test import SimpleTestCase
from django.db.models.expressions import SimpleCol, F
from django.db.models.sql.query import Query
from .models import Item

class TestResolveLookupValueNestedIterables(SimpleTestCase):

    def test_nested_list_resolves_inner_f(self):
        q = Query(Item)
        value = [['x', F('id')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][1], SimpleCol)

    def test_nested_tuple_resolves_inner_f_and_preserves_tuple(self):
        q = Query(Item)
        value = (['a', F('id')],)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][1], SimpleCol)

    def test_list_containing_tuple_with_f(self):
        q = Query(Item)
        value = [('foo', (F('id'),))]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][1][0], SimpleCol)

    def test_tuple_of_tuples_nested_f_resolution(self):
        q = Query(Item)
        value = ((('a', F('id')),),)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], tuple)
        self.assertIsInstance(result[0][0][1], SimpleCol)

    def test_deeper_nesting_resolves_all_levels(self):
        q = Query(Item)
        value = [[['deep', F('id')]]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], list)
        self.assertIsInstance(result[0][0][1], SimpleCol)

    def test_mixed_nested_structures(self):
        q = Query(Item)
        value = (['a', (F('id'), ['b', F('created')])],)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        inner = result[0]
        self.assertIsInstance(inner, list)
        self.assertIsInstance(inner[1], tuple)
        self.assertIsInstance(inner[1][0], SimpleCol)
        self.assertIsInstance(inner[1][1], list)
        self.assertIsInstance(inner[1][1][1], SimpleCol)

    def test_multiple_f_in_nested_list(self):
        q = Query(Item)
        value = [[F('id'), F('created')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertIsInstance(result[0][1], SimpleCol)

    def test_nested_iterables_with_none_and_f(self):
        q = Query(Item)
        value = [[None, F('id')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsNone(result[0][0])
        self.assertIsInstance(result[0][1], SimpleCol)

from django.db.models.expressions import Col, SimpleCol, F
from django.db.models.expressions import Col, SimpleCol, F
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from .models import Item, Author

class TestResolveLookupValueNestedIterables(SimpleTestCase):

    def test_nested_list_of_list_with_F_simple_col_true(self):
        q = Query(Item)
        val = [[F('created')], F('modified')]
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1], SimpleCol)

    def test_nested_tuple_of_tuple_with_F(self):
        q = Query(Item)
        val = ((F('created'),),)
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_deeply_nested_iterable_resolves_inner_F(self):
        q = Query(Item)
        val = [[[F('created')]]]
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)

    def test_mixed_scalars_and_exprs_in_nested_iterable(self):
        q = Query(Item)
        val = [1, [F('created'), 2]]
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertEqual(resolved[0], 1)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[1][1], 2)

    def test_preserve_mixed_tuple_and_list_types(self):
        q = Query(Item)
        val = ([F('created')],)
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_nested_iterables_multiple_exprs_resolve_all(self):
        q = Query(Item)
        val = [[F('created'), F('modified')], (F('created'),)]
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[0][1], SimpleCol)
        self.assertIsInstance(resolved[1][0], SimpleCol)

    def test_nested_iterable_on_different_model_field(self):
        q = Query(Author)
        val = [[F('id')], F('num')]
        resolved = q.resolve_lookup_value(val, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1], SimpleCol)

from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from .models import Author, Item

class TestQueryResolveLookupValueNested(SimpleTestCase):

    def test_nested_tuple_inside_list_resolves_F(self):
        q = Query(Author)
        value = [(F('id'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_nested_list_inside_tuple_resolves_F(self):
        q = Query(Author)
        value = ([F('id')],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_three_level_nesting_resolves_F_deeply(self):
        q = Query(Author)
        value = [[(F('id'),)]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], tuple)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)

    def test_mixed_values_and_expressions_in_nested_containers(self):
        q = Query(Author)
        value = [(F('id'), 'x'), ('y', F('id'))]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertEqual(resolved[0][1], 'x')
        self.assertEqual(resolved[1][0], 'y')
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1][1], SimpleCol)

    def test_deep_mixed_nesting_resolves_all_expressions(self):
        q = Query(Author)
        value = ([('a', [F('id')])],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        inner = resolved[0]
        self.assertIsInstance(inner, list)
        nested_tuple = inner[0]
        self.assertIsInstance(nested_tuple, tuple)
        nested_list = nested_tuple[1]
        self.assertIsInstance(nested_list, list)
        self.assertIsInstance(nested_list[0], SimpleCol)

    def test_tuple_of_lists_with_inner_Fs(self):
        q = Query(Item)
        value = ([F('created')], [F('modified')])
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1][0], SimpleCol)

    def test_deep_uniform_list_nesting_resolves_all_levels(self):
        q = Query(Author)
        value = [[[F('id')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)

from django.test import SimpleTestCase
from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item

class TestResolveLookupValueNested(SimpleTestCase):

    def test_resolve_lookup_value_nested_list_resolves_F(self):
        q = Query(Item)
        value = [[F('id')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('id'))

    def test_resolve_lookup_value_nested_tuple_resolves_F(self):
        q = Query(Item)
        value = ((F('id'),),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('id'))

    def test_resolve_lookup_value_mixed_nested_structures(self):
        q = Query(Item)
        value = [F('id'), [F('created')], (F('id'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], SimpleCol)
        self.assertEqual(resolved[0].target, Item._meta.get_field('id'))
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[1][0].target, Item._meta.get_field('created'))
        self.assertIsInstance(resolved[2], tuple)
        self.assertIsInstance(resolved[2][0], SimpleCol)

    def test_resolve_lookup_value_deep_nesting(self):
        q = Query(Item)
        value = [[[F('id')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)
        self.assertEqual(resolved[0][0][0].target, Item._meta.get_field('id'))

    def test_resolve_lookup_value_preserves_list_type_with_nested(self):
        q = Query(Item)
        value = [[F('id'), F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertEqual(len(resolved[0]), 2)
        self.assertTrue(all((isinstance(c, SimpleCol) for c in resolved[0])))

    def test_resolve_lookup_value_preserves_tuple_type_with_nested(self):
        q = Query(Item)
        value = ((F('id'), F('created')),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertEqual(len(resolved[0]), 2)
        self.assertTrue(all((isinstance(c, SimpleCol) for c in resolved[0])))

    def test_resolve_lookup_value_multiple_inner_items(self):
        q = Query(Item)
        value = [[F('id'), F('id'), F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertEqual(len(resolved[0]), 3)
        self.assertTrue(all((isinstance(c, SimpleCol) for c in resolved[0])))

    def test_resolve_lookup_value_nested_tuple_in_list(self):
        q = Query(Item)
        value = [(F('id'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

from django.test import SimpleTestCase
from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from .models import Item


class TestResolveLookupValueNested(SimpleTestCase):
    def test_nested_list_with_F(self):
        q = Query(Item)
        value = [['a', F('id')]]
        res = q.resolve_lookup_value(value, None, True, True)
        # inner F('id') must be resolved to a SimpleCol
        self.assertIsInstance(res[0][1], SimpleCol)

    def test_nested_tuple_inside_list_with_F(self):
        q = Query(Item)
        value = [('a', F('id'))]
        res = q.resolve_lookup_value(value, None, True, True)
        # the tuple's second element should be resolved to a SimpleCol
        self.assertIsInstance(res[0][1], SimpleCol)

    def test_list_inside_tuple_with_F(self):
        q = Query(Item)
        value = (['x', F('id')],)
        res = q.resolve_lookup_value(value, None, True, True)
        # outer is tuple, inner list element at index 1 resolved
        self.assertIsInstance(res[0][1], SimpleCol)

    def test_tuple_of_tuple_with_F(self):
        q = Query(Item)
        value = ((F('id'), 'z'),)
        res = q.resolve_lookup_value(value, None, True, True)
        # nested F inside tuple should be resolved
        self.assertIsInstance(res[0][0], SimpleCol)

    def test_deeply_nested_mixed_containers(self):
        q = Query(Item)
        value = [[(F('id'),),],]
        res = q.resolve_lookup_value(value, None, True, True)
        # access down three levels to find resolved SimpleCol
        self.assertIsInstance(res[0][0][0], SimpleCol)

    def test_multiple_nested_elements_mixed(self):
        q = Query(Item)
        value = [F('id'), ['a', F('created')], ('b', F('modified'))]
        res = q.resolve_lookup_value(value, None, True, True)
        # first element resolved
        self.assertIsInstance(res[0], SimpleCol)
        # nested list element resolved
        self.assertIsInstance(res[1][1], SimpleCol)
        # nested tuple element resolved
        self.assertIsInstance(res[2][1], SimpleCol)

    def test_preserve_outer_type_list_of_tuple(self):
        q = Query(Item)
        value = [('a', F('id'))]
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, list)
        # inner tuple should have resolved element
        self.assertIsInstance(res[0][1], SimpleCol)

    def test_preserve_outer_type_tuple_of_list(self):
        q = Query(Item)
        value = (['a', F('id')],)
        res = q.resolve_lookup_value(value, None, True, True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0][1], SimpleCol)

    def test_deep_three_level_tuple_list_tuple(self):
        q = Query(Item)
        value = (['x', (F('id'),)],)
        res = q.resolve_lookup_value(value, None, True, True)
        # drill down and ensure the deepest F is resolved
        self.assertIsInstance(res[0][1][0], SimpleCol)

    def test_mixed_nested_empty_and_expressions(self):
        q = Query(Item)
        value = [[], (F('id'),), ['a', [] , (F('created'),)]]
        res = q.resolve_lookup_value(value, None, True, True)
        # empty containers preserved, but F instances resolved wherever present
        self.assertEqual(res[0], [])
        self.assertIsInstance(res[1][0], SimpleCol)
        self.assertIsInstance(res[2][2][0], SimpleCol)

from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from .models import Author

class ResolveLookupValueTests(SimpleTestCase):

    def test_nested_list_single_F(self):
        q = Query(Author)
        value = [[F('id')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_nested_tuple_single_F(self):
        q = Query(Author)
        value = ((F('id'),),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_mixed_list_and_tuple_nested(self):
        q = Query(Author)
        value = [(F('id'),), [F('num')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)

    def test_deeply_nested_three_levels(self):
        q = Query(Author)
        value = [[[F('id')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)

    def test_non_expression_scalars_and_nested(self):
        q = Query(Author)
        value = [1, [F('id'), 2], 'a']
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertEqual(resolved[0], 1)
        self.assertEqual(resolved[2], 'a')
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[1][1], 2)

    def test_outer_tuple_preserved_with_inner_list(self):
        q = Query(Author)
        value = ([F('id')],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_inner_container_types_preserved(self):
        q = Query(Author)
        value = ([(F('id'),)],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        inner_list = resolved[0]
        self.assertIsInstance(inner_list, list)
        inner_tuple = inner_list[0]
        self.assertIsInstance(inner_tuple, tuple)
        self.assertIsInstance(inner_tuple[0], SimpleCol)

    def test_multiple_nested_expressions(self):
        q = Query(Author)
        value = [[F('id'), F('id')], (F('id'), [F('id')])]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[0][1], SimpleCol)
        self.assertIsInstance(resolved[1], tuple)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertIsInstance(resolved[1][1], list)
        self.assertIsInstance(resolved[1][1][0], SimpleCol)

from django.test import SimpleTestCase
from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from .models import Item

class ResolveLookupValueTests(SimpleTestCase):

    def test_nested_list_resolves_inner_list_F(self):
        q = Query(Item)
        value = [[F('created')], [F('modified')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(result[1][0].target, Item._meta.get_field('modified'))

    def test_list_with_inner_tuple_resolves_inner_tuple_F(self):
        q = Query(Item)
        value = [(F('created'),), (F('modified'),)]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[1], tuple)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(result[1][0].target, Item._meta.get_field('modified'))

    def test_deeply_nested_mixed_structures_resolve_all_Fs(self):
        q = Query(Item)
        value = ([F('created'), (F('modified'),)],)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        inner = result[0]
        self.assertIsInstance(inner, list)
        self.assertIsInstance(inner[0], SimpleCol)
        self.assertEqual(inner[0].target, Item._meta.get_field('created'))
        self.assertIsInstance(inner[1], tuple)
        self.assertIsInstance(inner[1][0], SimpleCol)
        self.assertEqual(inner[1][0].target, Item._meta.get_field('modified'))

    def test_mixed_expressions_and_literals_in_list(self):
        q = Query(Item)
        value = ['x', F('created'), (1, F('modified'))]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], 'x')
        self.assertIsInstance(result[1], SimpleCol)
        self.assertEqual(result[1].target, Item._meta.get_field('created'))
        self.assertIsInstance(result[2], tuple)
        self.assertEqual(result[2][0], 1)
        self.assertIsInstance(result[2][1], SimpleCol)
        self.assertEqual(result[2][1].target, Item._meta.get_field('modified'))

    def test_various_nested_combinations_resolve_all_Fs(self):
        q = Query(Item)
        value = ([F('created')], (F('modified'),), [(F('created'), ['y', F('modified')])])
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))
        self.assertIsInstance(result[1], tuple)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertEqual(result[1][0].target, Item._meta.get_field('modified'))
        third = result[2]
        self.assertIsInstance(third, list)
        inner_tuple = third[0]
        self.assertIsInstance(inner_tuple, tuple)
        self.assertIsInstance(inner_tuple[0], SimpleCol)
        self.assertEqual(inner_tuple[0].target, Item._meta.get_field('created'))
        self.assertIsInstance(inner_tuple[1], list)
        self.assertEqual(inner_tuple[1][0], 'y')
        self.assertIsInstance(inner_tuple[1][1], SimpleCol)
        self.assertEqual(inner_tuple[1][1].target, Item._meta.get_field('modified'))

from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from .models import Item

class TestResolveLookupValueNested(SimpleTestCase):

    def test_nested_list_with_inner_list_and_Fs_resolves(self):
        q = Query(Item)
        value = [[F('created')], F('modified')]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1], SimpleCol)

    def test_nested_tuple_outer_preserved_and_inner_tuple_resolved(self):
        q = Query(Item)
        value = ((F('created'),),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_mixed_list_and_tuple_preserve_types_and_resolve(self):
        q = Query(Item)
        value = [(F('created'),), [F('modified')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)

    def test_deeply_nested_iterables_resolve_all_Fs(self):
        q = Query(Item)
        value = [[[F('created')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)

    def test_inner_non_expression_values_are_untouched(self):
        q = Query(Item)
        value = [['a', F('created')], 'b']
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertEqual(resolved[0][0], 'a')
        self.assertIsInstance(resolved[0][1], SimpleCol)
        self.assertEqual(resolved[1], 'b')

    def test_preserve_inner_tuple_when_outer_is_list(self):
        q = Query(Item)
        value = [(F('created'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_preserve_inner_list_when_outer_is_tuple(self):
        q = Query(Item)
        value = ([F('created')],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)

    def test_multiple_levels_mixed_types_resolve(self):
        q = Query(Item)
        value = ([(F('created'),), [F('modified')]],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        inner = resolved[0]
        self.assertIsInstance(inner, list)
        self.assertIsInstance(inner[0], tuple)
        self.assertIsInstance(inner[0][0], SimpleCol)
        self.assertIsInstance(inner[1], list)
        self.assertIsInstance(inner[1][0], SimpleCol)

    def test_resolve_lookup_value_with_multiple_nested_levels_and_literals(self):
        q = Query(Item)
        value = [('x', [F('created')]), (['y'], ('z', F('modified')))]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertEqual(resolved[0][0], 'x')
        self.assertIsInstance(resolved[0][1], list)
        self.assertIsInstance(resolved[0][1][0], SimpleCol)
        self.assertIsInstance(resolved[1], tuple)
        self.assertIsInstance(resolved[1][0], list)
        self.assertEqual(resolved[1][0][0], 'y')
        self.assertIsInstance(resolved[1][1], tuple)
        self.assertEqual(resolved[1][1][0], 'z')
        self.assertIsInstance(resolved[1][1][1], SimpleCol)

from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from .models import Item

class TestQueryNestedResolveLookupValue(SimpleTestCase):

    def test_nested_list_depth2_resolves_F(self):
        q = Query(Item)
        value = [[F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertEqual(len(resolved), 1)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_nested_tuple_depth2_resolves_F(self):
        q = Query(Item)
        value = ((F('created'),),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertEqual(len(resolved), 1)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_list_with_inner_tuple_preserves_inner_type(self):
        q = Query(Item)
        value = [(F('created'),)]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_tuple_with_inner_list_preserves_inner_type(self):
        q = Query(Item)
        value = ([F('created')],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))

    def test_mixed_nested_iterables_resolve_all_expressions(self):
        q = Query(Item)
        value = [(F('created'),), [F('modified')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(resolved[1][0].target, Item._meta.get_field('modified'))

    def test_nested_depth3_resolves_deep_expression(self):
        q = Query(Item)
        value = [[[F('created')]]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)
        self.assertEqual(resolved[0][0][0].target, Item._meta.get_field('created'))

    def test_mixed_literals_and_expressions_in_inner_iterable(self):
        q = Query(Item)
        value = [['x', F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0][0], str)
        self.assertIsInstance(resolved[0][1], SimpleCol)
        self.assertEqual(resolved[0][1].target, Item._meta.get_field('created'))

    def test_empty_inner_iterable_preserved(self):
        q = Query(Item)
        value = [[], [F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertEqual(len(resolved[0]), 0)
        self.assertIsInstance(resolved[1][0], SimpleCol)

    def test_deep_tuple_and_list_mixture_resolves(self):
        q = Query(Item)
        value = (([F('created')],),)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], tuple)
        self.assertIsInstance(resolved[0][0], list)
        self.assertIsInstance(resolved[0][0][0], SimpleCol)
        self.assertEqual(resolved[0][0][0].target, Item._meta.get_field('created'))

from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from django.test import SimpleTestCase
from .models import Item

class TestQueryNestedResolve(SimpleTestCase):

    def test_nested_list_with_F_resolved(self):
        q = Query(Item)
        res = q.resolve_lookup_value([[F('id')]], can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0][0], SimpleCol)
        self.assertEqual(res[0][0].target, Item._meta.get_field('id'))

    def test_nested_tuple_with_F_resolved_and_types(self):
        q = Query(Item)
        value = ((F('id'),),)
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][0], SimpleCol)
        self.assertEqual(res[0][0].target, Item._meta.get_field('id'))

    def test_inner_tuple_preserved_in_list(self):
        q = Query(Item)
        value = [(F('id'),)]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][0], SimpleCol)
        self.assertEqual(res[0][0].target, Item._meta.get_field('id'))

    def test_multiple_Fs_in_nested_tuple(self):
        q = Query(Item)
        value = [(F('created'), F('modified'))]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        inner = res[0]
        self.assertIsInstance(inner[0], SimpleCol)
        self.assertIsInstance(inner[1], SimpleCol)
        self.assertEqual(inner[0].target, Item._meta.get_field('created'))
        self.assertEqual(inner[1].target, Item._meta.get_field('modified'))

    def test_deeply_nested_two_levels(self):
        q = Query(Item)
        value = [[[F('id')]]]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], list)
        self.assertIsInstance(res[0][0][0], SimpleCol)
        self.assertEqual(res[0][0][0].target, Item._meta.get_field('id'))

    def test_mixed_values_and_Fs_nested(self):
        q = Query(Item)
        value = [('a', F('id'))]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertEqual(res[0][0], 'a')
        self.assertIsInstance(res[0][1], SimpleCol)
        self.assertEqual(res[0][1].target, Item._meta.get_field('id'))

    def test_nested_tuple_of_lists(self):
        q = Query(Item)
        value = ([F('id')],)
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, tuple)
        self.assertIsInstance(res[0], list)
        self.assertIsInstance(res[0][0], SimpleCol)
        self.assertEqual(res[0][0].target, Item._meta.get_field('id'))

    def test_nested_list_of_tuples_deep(self):
        q = Query(Item)
        value = [((F('id'),),)]
        res = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], tuple)
        self.assertIsInstance(res[0][0], tuple)
        self.assertIsInstance(res[0][0][0], SimpleCol)
        self.assertEqual(res[0][0][0].target, Item._meta.get_field('id'))

from django.test import SimpleTestCase
from django.db.models import F
from django.db.models.expressions import SimpleCol
from django.db.models.sql.query import Query
from .models import Item

def _contains_instance(obj, cls):
    """
    Recursively search nested iterables for an instance of cls.
    """
    if isinstance(obj, cls):
        return True
    if isinstance(obj, (list, tuple)):
        return any((_contains_instance(v, cls) for v in obj))
    return False

from django.db.models.expressions import Col
from django.test import SimpleTestCase
from django.db.models.expressions import SimpleCol
from django.db.models import F
from django.db.models.sql.query import Query
from .models import Item


class TestResolveLookupValueRecursive(SimpleTestCase):
    def test_nested_list_of_list_with_f(self):
        q = Query(Item)
        value = [[F('created')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_nested_tuple_of_tuple_with_f(self):
        q = Query(Item)
        value = ((F('created'),),)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_list_of_tuple_with_f_inside_tuple(self):
        q = Query(Item)
        value = [(F('created'), 5)]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][1], 5)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_tuple_of_list_with_f_inside_list(self):
        q = Query(Item)
        value = ([F('created')],)
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], SimpleCol)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_deeply_nested_three_levels(self):
        q = Query(Item)
        value = [[[F('created')]]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[0][0], list)
        self.assertIsInstance(result[0][0][0], SimpleCol)
        self.assertEqual(result[0][0][0].target, Item._meta.get_field('created'))

    def test_mixed_nested_structures(self):
        q = Query(Item)
        value = [F('created'), [F('created'), [F('created')]]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        # outer preserved as list
        self.assertIsInstance(result, list)
        # first element resolved
        self.assertIsInstance(result[0], SimpleCol)
        # nested resolved
        self.assertIsInstance(result[1], list)
        self.assertIsInstance(result[1][0], SimpleCol)
        self.assertIsInstance(result[1][1], list)
        self.assertIsInstance(result[1][1][0], SimpleCol)

    def test_non_expression_elements_preserved(self):
        q = Query(Item)
        value = [[1, 'a', F('created')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(result[0][1], 'a')
        self.assertIsInstance(result[0][2], SimpleCol)

    def test_simple_col_flag_false_resolves_to_col(self):
        # When simple_col is False, F() should resolve to a Col-like (not SimpleCol).
        from django.db.models.expressions import Col
        q = Query(Item)
        value = [[F('created')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=False)
        self.assertIsInstance(result[0][0], Col)
        self.assertEqual(result[0][0].target, Item._meta.get_field('created'))

    def test_nested_tuples_with_mixed_types(self):
        q = Query(Item)
        value = ((1, F('created')), ('x', (F('created'), 2)))
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0][0], 1)
        self.assertIsInstance(result[0][1], SimpleCol)
        self.assertEqual(result[1][0], 'x')
        self.assertIsInstance(result[1][1][0], SimpleCol)
        self.assertEqual(result[1][1][1], 2)

    def test_empty_and_nonempty_nested_lists(self):
        q = Query(Item)
        value = [[], [F('created')]]
        result = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0], [])
        self.assertIsInstance(result[1][0], SimpleCol)

from datetime import datetime
from django.core.exceptions import FieldError
from django.db.models import CharField, F, Q
from django.db.models.expressions import SimpleCol
from django.db.models.fields.related_lookups import RelatedIsNull
from django.db.models.functions import Lower
from django.db.models.lookups import Exact, GreaterThan, IsNull, LessThan
from django.db.models.sql.query import Query
from django.db.models.sql.where import OR
from django.test import SimpleTestCase
from django.test.utils import register_lookup
from .models import Author, Item, ObjectC, Ranking

class TestQuery(SimpleTestCase):

    def test_resolve_lookup_value_nested_list_resolves_F_to_SimpleCol(self):
        q = Query(Item)
        value = ['a', [F('created')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[1], list)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[1][0].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_nested_tuple_resolves_F_to_SimpleCol(self):
        q = Query(Item)
        value = ('x', (F('modified'),))
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[1], tuple)
        self.assertIsInstance(resolved[1][0], SimpleCol)
        self.assertEqual(resolved[1][0].target, Item._meta.get_field('modified'))

    def test_resolve_lookup_value_deep_mixed_nesting(self):
        q = Query(Item)
        value = ([('a', F('created'))],)
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, tuple)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], tuple)
        self.assertIsInstance(resolved[0][0][1], SimpleCol)
        self.assertEqual(resolved[0][0][1].target, Item._meta.get_field('created'))

    def test_resolve_lookup_value_multiple_expressions_in_nested(self):
        q = Query(Item)
        value = [[F('created'), F('modified')]]
        resolved = q.resolve_lookup_value(value, can_reuse=None, allow_joins=True, simple_col=True)
        self.assertIsInstance(resolved, list)
        self.assertIsInstance(resolved[0], list)
        self.assertIsInstance(resolved[0][0], SimpleCol)
        self.assertIsInstance(resolved[0][1], SimpleCol)
        self.assertEqual(resolved[0][0].target, Item._meta.get_field('created'))
        self.assertEqual(resolved[0][1].target, Item._meta.get_field('modified'))
new_imports_code: ''