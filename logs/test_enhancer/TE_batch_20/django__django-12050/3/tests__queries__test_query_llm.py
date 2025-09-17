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