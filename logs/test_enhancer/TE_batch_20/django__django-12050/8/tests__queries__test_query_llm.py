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