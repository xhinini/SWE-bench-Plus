from types import SimpleNamespace
from types import SimpleNamespace
from django.test import SimpleTestCase
from django.db import models

class FieldOrderingRegressionTests(SimpleTestCase):

    def test_unbound_less_than_bound_when_creation_counter_equal(self):
        """
        A Field without a model should compare as less-than a Field with a model
        when both have the same creation_counter (no-model fields ordered first).
        """
        f_unbound = models.Field()
        f_bound = models.Field()
        f_unbound.creation_counter = 12345
        f_bound.creation_counter = 12345
        f_bound.model = self.make_model('app', 'm1')
        self.assertLess(f_unbound, f_bound)

    def test_sorting_stable_with_unbound_and_bound_fields(self):
        """
        Sorting a mixture of bound and unbound Fields with equal creation_counter
        should place unbound fields first, and then bound fields ordered by
        (app_label, model_name).
        """
        cc = 77777
        f_unbound = models.Field()
        f_unbound.creation_counter = cc
        f_bound_a = models.Field()
        f_bound_a.creation_counter = cc
        f_bound_b = models.Field()
        f_bound_b.creation_counter = cc
        f_bound_a.model = self.make_model('aaa', 'alpha')
        f_bound_b.model = self.make_model('bbb', 'beta')
        arr = [f_bound_b, f_unbound, f_bound_a]
        sorted_arr = sorted(arr)
        self.assertEqual(sorted_arr, [f_unbound, f_bound_a, f_bound_b])

    def test_unbound_not_greater_than_bound(self):
        """
        Confirm that the unbound field is not considered greater than the bound
        field when creation_counters are equal (sanity check of ordering direction).
        """
        f_unbound = models.Field()
        f_bound = models.Field()
        f_unbound.creation_counter = 9999
        f_bound.creation_counter = 9999
        f_bound.model = self.make_model('app', 'mm')
        self.assertFalse(f_unbound > f_bound)
        self.assertTrue(f_bound > f_unbound)

import heapq
import bisect
from django.test import SimpleTestCase
from django.db import models
from django.utils import timezone
import heapq
import bisect
from .models import Foo, Bar

class FieldOrderingRegressionTests(SimpleTestCase):

    def setUp(self):
        self.no_model_field = models.Field()
        self.with_model_field = models.Field()
        self.no_model_field.creation_counter = 999999
        self.with_model_field.creation_counter = 999999
        if hasattr(self.no_model_field, 'model'):
            delattr(self.no_model_field, 'model')
        self.with_model_field.model = Foo

    def test_no_model_lt_with_model_direct(self):
        self.assertTrue(self.no_model_field < self.with_model_field)

    def test_sorted_places_no_model_first(self):
        items = [self.with_model_field, self.no_model_field]
        sorted_items = sorted(items)
        self.assertIs(sorted_items[0], self.no_model_field)
        self.assertIs(sorted_items[1], self.with_model_field)

    def test_list_sort_places_no_model_first(self):
        items = [self.with_model_field, self.no_model_field]
        items.sort()
        self.assertIs(items[0], self.no_model_field)
        self.assertIs(items[1], self.with_model_field)

    def test_min_returns_no_model(self):
        items = [self.with_model_field, self.no_model_field]
        self.assertIs(min(items), self.no_model_field)

    def test_heapq_nsmallest_returns_no_model(self):
        items = [self.with_model_field, self.no_model_field]
        smallest = heapq.nsmallest(1, items)[0]
        self.assertIs(smallest, self.no_model_field)

    def test_sorted_three_fields_first_is_no_model(self):
        f_model_bar = models.Field()
        f_model_bar.creation_counter = 999999
        f_model_bar.model = Bar
        items = [f_model_bar, self.with_model_field, self.no_model_field]
        sorted_items = sorted(items)
        self.assertIs(sorted_items[0], self.no_model_field)
        self.assertIn(sorted_items[1], (self.with_model_field, f_model_bar))
        self.assertIn(sorted_items[2], (self.with_model_field, f_model_bar))

    def test_sort_stability_with_mixed_no_model_and_model_fields(self):
        nm1 = models.Field()
        nm1.creation_counter = 42
        nm2 = models.Field()
        nm2.creation_counter = 42
        if hasattr(nm1, 'model'):
            delattr(nm1, 'model')
        if hasattr(nm2, 'model'):
            delattr(nm2, 'model')
        m1 = models.Field()
        m1.creation_counter = 42
        m1.model = Foo
        m2 = models.Field()
        m2.creation_counter = 42
        m2.model = Bar
        mixed = [m1, nm1, m2, nm2]
        mixed.sort()
        self.assertTrue(all((not hasattr(x, 'model') for x in mixed[:2])))
        self.assertTrue(all((hasattr(x, 'model') for x in mixed[2:])))

import bisect
import bisect
from django.test import SimpleTestCase
from django.db import models

class FieldOrderingRegressionTests(SimpleTestCase):

    def test_unbound_field_orders_before_bound_field_when_counters_equal(self):
        """
        If two fields have the same creation_counter, an unbound field (no
        model) should be ordered before a bound field.
        """
        counter = 12345
        unbound = self._make_field(counter)
        bound = self._make_field(counter)
        bound, Model = self._attach_field_to_model(bound, 'ModelX', 'app_x', 'f_bound')
        self.assertTrue(unbound < bound)
        lst = [bound, unbound]
        lst.sort()
        self.assertIs(lst[0], unbound)
        self.assertIs(lst[1], bound)

    def test_bound_field_greater_than_unbound_field_when_counters_equal(self):
        """
        The reverse comparison should yield the opposite ordering.
        """
        counter = 20000
        bound = self._make_field(counter)
        unbound = self._make_field(counter)
        bound, Model = self._attach_field_to_model(bound, 'ModelY', 'app_y', 'f_bound2')
        self.assertTrue(unbound < bound)
        self.assertTrue(bound > unbound)

    def test_sorting_mixed_fields_preserves_unbound_first(self):
        """
        Sorting a list with multiple fields having identical creation_counter
        values should place all unbound fields before bound fields.
        """
        counter = 30000
        fields = [self._make_field(counter) for _ in range(4)]
        fields[1], M1 = self._attach_field_to_model(fields[1], 'M1', 'app_a', 'a1')
        fields[3], M2 = self._attach_field_to_model(fields[3], 'M2', 'app_b', 'b1')
        before_sort = list(fields)
        fields.sort()
        self.assertFalse(hasattr(fields[0], 'model'))
        self.assertFalse(hasattr(fields[1], 'model'))
        self.assertTrue(hasattr(fields[2], 'model'))
        self.assertTrue(hasattr(fields[3], 'model'))
        self.assertCountEqual(fields, before_sort)

    def test_bisect_insertion_preserves_order_for_equal_counters(self):
        """
        bisect.insort should insert elements preserving the intended order
        (unbound fields before bound fields) when creation_counter values
        are equal.
        """
        counter = 40000
        bound = self._make_field(counter)
        unbound = self._make_field(counter)
        bound, M = self._attach_field_to_model(bound, 'MB', 'app_z', 'fb')
        lst = []
        bisect.insort(lst, bound)
        bisect.insort(lst, unbound)
        self.assertIs(lst[0], unbound)
        self.assertIs(lst[1], bound)

    def test_transitive_ordering_unbound_modelA_modelB(self):
        """
        With three fields (unbound, modelA, modelB) all sharing the same
        creation_counter, ordering should be: unbound < modelA < modelB
        when modelA's app_label/model_name sorts before modelB's tuple.
        """
        counter = 50000
        unbound = self._make_field(counter)
        fa = self._make_field(counter)
        fb = self._make_field(counter)
        fa, A = self._attach_field_to_model(fa, 'Alpha', 'app_alpha', 'field_a')
        fb, B = self._attach_field_to_model(fb, 'Beta', 'app_beta', 'field_b')
        self.assertTrue(unbound < fa)
        self.assertTrue(fa < fb)
        lst = [fb, fa, unbound]
        lst.sort()
        self.assertIs(lst[0], unbound)
        self.assertIs(lst[1], fa)
        self.assertIs(lst[2], fb)

    def test_multiple_unbound_and_bound_sorting_stability(self):
        """
        Ensure sorting is stable and places all unbound fields before any bound
        fields even when interleaved in the input list.
        """
        counter = 60000
        items = []
        for i in range(6):
            f = self._make_field(counter)
            if i % 2 == 0:
                f, _ = self._attach_field_to_model(f, f'M{i}', f'app{i}', f'fld{i}')
            items.append(f)
        original_items = list(items)
        items.sort()
        bound_flags = [hasattr(x, 'model') for x in items]
        if any(bound_flags):
            first_bound_index = bound_flags.index(True)
            self.assertTrue(all((flag is True for flag in bound_flags[first_bound_index:])))
        self.assertCountEqual(items, original_items)

    def test_sorting_mixed_many_entries(self):
        """
        Larger mixed list sorting: create several unbound and several bound
        fields, ensure all unbound come first and that sorting is deterministic.
        """
        counter = 90000
        unbound_list = [self._make_field(counter) for _ in range(3)]
        bound_list = []
        for i in range(3):
            f = self._make_field(counter)
            f, _ = self._attach_field_to_model(f, f'M{i}', f'app_z{i}', f'fld{i}')
            bound_list.append(f)
        combined = []
        for u, b in zip(unbound_list, bound_list):
            combined.extend([b, u])
        combined.sort()
        for idx, item in enumerate(combined[:3]):
            self.assertFalse(hasattr(item, 'model'), msg=f'Item at {idx} unexpectedly bound')
        for idx, item in enumerate(combined[3:]):
            self.assertTrue(hasattr(item, 'model'), msg=f'Item at {idx + 3} unexpectedly unbound')

from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class FieldModelPresenceOrderingTests(SimpleTestCase):

    def test_bound_field_greater_than_unbound_field_equal_creation_counter(self):
        bound = Bar._meta.get_field('a')
        unbound = models.CharField(max_length=10)
        restore = self._set_and_restore_counters((bound, unbound), 424242)
        try:
            self.assertTrue(unbound < bound)
            self.assertFalse(bound < unbound)
        finally:
            restore()

    def test_sort_bound_then_unbound_multiple_times(self):
        bound1 = Foo._meta.get_field('a')
        bound2 = Bar._meta.get_field('a')
        unbound1 = models.CharField(max_length=5)
        unbound2 = models.IntegerField()
        restore = self._set_and_restore_counters((bound1, bound2, unbound1, unbound2), 55555)
        try:
            initial = [bound1, bound2, unbound1, unbound2]
            sorted_list = sorted(initial)
            self.assertTrue(sorted_list[0] in (unbound1, unbound2))
            self.assertTrue(sorted_list[1] in (unbound1, unbound2))
            self.assertTrue(sorted_list[2] in (bound1, bound2))
            self.assertTrue(sorted_list[3] in (bound1, bound2))
        finally:
            restore()

    def test_comparison_commutativity_between_bound_and_unbound(self):
        bound = Foo._meta.get_field('a')
        unbound = models.TextField()
        restore = self._set_and_restore_counters((bound, unbound), 77777)
        try:
            self.assertTrue(unbound < bound)
            self.assertFalse(bound < unbound)
        finally:
            restore()

    def test_multiple_bound_and_unbound_stable_grouping(self):
        bound_foo = Foo._meta.get_field('a')
        bound_bar = Bar._meta.get_field('a')
        unbound_a = models.Field()
        unbound_b = models.CharField(max_length=3)
        restore = self._set_and_restore_counters((bound_foo, bound_bar, unbound_a, unbound_b), 202020)
        try:
            mixed = [bound_foo, unbound_a, bound_bar, unbound_b]
            sorted_mixed = sorted(mixed)
            first_two = sorted_mixed[:2]
            last_two = sorted_mixed[2:]
            self.assertTrue(all((isinstance(f, models.Field) for f in first_two)))
            self.assertTrue(all((hasattr(f, 'model') for f in last_two)))
        finally:
            restore()

from bisect import bisect_left
from bisect import bisect_left
from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class FieldOrderingRegressionTests(SimpleTestCase):

    def setUp(self):
        self.foo_field = Foo._meta.get_field('a')
        self.bar_field = Bar._meta.get_field('a')
        self.unbound1 = models.Field()
        self.unbound2 = models.Field()

    def _equalize_counter(self, *fields, value=12345):
        """
        Force the given Field instances to have the same creation_counter.
        This simulates the tie-breaker branch in __lt__ that compares model
        information when creation_counters are equal.
        """
        for f in fields:
            f.creation_counter = value

from django import forms
from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class AdditionalFieldOrderingTests(SimpleTestCase):

    def _make_equal_counters(self, *fields, value=42):
        for f in fields:
            f.creation_counter = value

    def test_no_model_field_less_than_model_field_equal_creation_counter(self):
        f_no = models.Field()
        f_model = models.Field()
        f_model.model = Foo
        self._make_equal_counters(f_no, f_model, value=1000)
        self.assertTrue(f_no < f_model)
        self.assertFalse(f_model < f_no)

    def test_sort_preserves_no_model_first_when_equal_creation_counter(self):
        f_no = models.Field()
        f_model = models.Field()
        f_model.model = Foo
        self._make_equal_counters(f_no, f_model, value=2000)
        ordered = sorted([f_model, f_no])
        self.assertIs(ordered[0], f_no)
        self.assertIs(ordered[1], f_model)

    def test_list_sort_inplace_puts_no_model_first(self):
        f_no = models.Field()
        f_model = models.Field()
        f_model.model = Foo
        self._make_equal_counters(f_no, f_model, value=3000)
        lst = [f_model, f_no]
        lst.sort()
        self.assertIs(lst[0], f_no)
        self.assertIs(lst[1], f_model)

    def test_multiple_items_sort_with_mixed_model_attachment(self):
        f_no1 = models.Field()
        f_no2 = models.Field()
        f_f1 = models.Field()
        f_f1.model = Foo
        f_b1 = models.Field()
        f_b1.model = Bar
        self._make_equal_counters(f_no1, f_no2, f_f1, f_b1, value=4000)
        lst = [f_f1, f_no2, f_b1, f_no1]
        sorted_lst = sorted(lst)
        self.assertIn(sorted_lst[0], (f_no1, f_no2))
        self.assertIn(sorted_lst[1], (f_no1, f_no2))
        self.assertIn(sorted_lst[2], (f_f1, f_b1))
        self.assertIn(sorted_lst[3], (f_f1, f_b1))

    def test_reverse_sort_places_model_fields_first(self):
        f_no = models.Field()
        f_model = models.Field()
        f_model.model = Foo
        self._make_equal_counters(f_no, f_model, value=5000)
        lst = [f_no, f_model]
        lst.sort(reverse=True)
        self.assertIs(lst[0], f_model)
        self.assertIs(lst[1], f_no)

    def test_comparison_with_unattached_and_attached_field_equals_logic(self):
        f_no = models.Field()
        f_model = models.Field()
        f_model.model = Foo
        self._make_equal_counters(f_no, f_model, value=6000)
        self.assertEqual(f_no < f_model, not f_model <= f_no)

    def test_comparison_when_only_one_field_has_model_attribute_but_is_falsey(self):
        f_no = models.Field()
        f_model_falsey = models.Field()

        class Dummy:

            def __bool__(self):
                return False
        dummy_model = Dummy()
        dummy_model._meta = type('Meta', (), {'app_label': 'x', 'model_name': 'y'})
        f_model_falsey.model = dummy_model
        self._make_equal_counters(f_no, f_model_falsey, value=9000)
        self.assertTrue(f_no < f_model_falsey)

import bisect
import bisect
from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class FieldOrderingRegressionTests(SimpleTestCase):

    def test_no_model_field_less_than_model_field(self):
        f_no = models.Field()
        f_with = models.Field()
        f_no.creation_counter = f_with.creation_counter = 12345
        f_with.model = Foo
        self.assertTrue(f_no < f_with)
        self.assertFalse(f_with < f_no)

    def test_model_field_greater_than_no_model_field_when_reversed(self):
        f_no = models.Field()
        f_with = models.Field()
        f_no.creation_counter = f_with.creation_counter = 12346
        f_with.model = Foo
        lst = [f_with, f_no]
        self.assertEqual(sorted(lst), [f_no, f_with])

    def test_sort_mixed_fields_places_no_model_first(self):
        f_no = models.Field()
        f_with = models.Field()
        f_no.creation_counter = f_with.creation_counter = 20000
        f_with.model = Foo
        sorted_list = sorted([f_with, f_no])
        self.assertEqual(sorted_list, [f_no, f_with])

from .models import Foo, Bar
from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class FieldOrderingHashTests(SimpleTestCase):

    def _make_field(self, creation_counter=None, model=None):
        f = models.Field()
        if creation_counter is not None:
            f.creation_counter = creation_counter
        if model is not None:
            f.model = model
        return f

    def test_no_model_less_than_model_with_same_creation_counter(self):
        f_no_model = self._make_field(creation_counter=999)
        f_with_model = self._make_field(creation_counter=999, model=Foo)
        self.assertTrue(hasattr(f_with_model, 'model'))
        self.assertFalse(hasattr(f_no_model, 'model'))
        self.assertLess(f_no_model, f_with_model)
        self.assertGreater(f_with_model, f_no_model)

    def test_sorting_list_with_mixed_models_places_no_model_first(self):
        fields = [self._make_field(creation_counter=42, model=Foo), self._make_field(creation_counter=42), self._make_field(creation_counter=42, model=Bar)]
        sorted_fields = sorted(fields)
        self.assertFalse(hasattr(sorted_fields[0], 'model'))
        self.assertTrue(hasattr(sorted_fields[1], 'model'))
        self.assertTrue(hasattr(sorted_fields[2], 'model'))

    def test_hash_equality_for_fields_with_same_model(self):
        f1 = self._make_field(creation_counter=55, model=Foo)
        f2 = self._make_field(creation_counter=55, model=Foo)
        expected = hash((55, Foo._meta.app_label, Foo._meta.model_name))
        self.assertEqual(hash(f1), expected)
        self.assertEqual(hash(f2), expected)

    def test_hash_difference_with_and_without_model(self):
        f_no_model = self._make_field(creation_counter=77)
        f_with_model = self._make_field(creation_counter=77, model=Foo)
        expected_with = hash((77, Foo._meta.app_label, Foo._meta.model_name))
        expected_no = hash((77, None, None))
        self.assertEqual(hash(f_with_model), expected_with)
        self.assertEqual(hash(f_no_model), expected_no)
        self.assertNotEqual(hash(f_no_model), hash(f_with_model))

    def test_exact_hash_matches_model_meta_tuple(self):
        f = self._make_field(creation_counter=314, model=Bar)
        expected_tuple = (314, Bar._meta.app_label, Bar._meta.model_name)
        self.assertEqual(hash(f), hash(expected_tuple))

import bisect
from django.test import SimpleTestCase
from django.db import models
from .models import Foo, Bar

class FieldOrderingRegressionTests(SimpleTestCase):
    """
    Regression tests for Field ordering/hash/equality behavior when
    creation_counter values are equal and fields may or may not be bound
    to a model (have a .model attribute).
    """

    def test_unbound_field_is_less_than_bound_field_when_creation_counter_equal(self):
        c = 99999
        f_no = self._make_unbound(c)
        f_model = self._make_bound(Foo, c)
        self.assertTrue(f_no < f_model)

    def test_sorted_swaps_bound_and_unbound_when_creation_counter_equal(self):
        c = 100001
        f_no = self._make_unbound(c)
        f_model = self._make_bound(Foo, c)
        lst = [f_model, f_no]
        sorted_lst = sorted(lst)
        self.assertEqual(sorted_lst, [f_no, f_model])

    def test_inplace_sort_swaps_bound_and_unbound_when_creation_counter_equal(self):
        c = 100002
        f_no = self._make_unbound(c)
        f_model = self._make_bound(Foo, c)
        lst = [f_model, f_no]
        lst.sort()
        self.assertEqual(lst, [f_no, f_model])

    def test_bisect_insertion_places_unbound_before_bound(self):
        c = 100005
        f_no = self._make_unbound(c)
        f_model = self._make_bound(Foo, c)
        lst = [f_model]
        bisect.insort(lst, f_no)
        self.assertEqual(lst, [f_no, f_model])

    def test_sort_with_multiple_mixed_places_all_unbound_before_models(self):
        c = 100006
        f_no1 = self._make_unbound(c)
        f_no2 = self._make_unbound(c)
        f_model1 = self._make_bound(Foo, c)
        f_model2 = self._make_bound(Bar, c)
        lst = [f_model1, f_model2, f_no1, f_no2]
        lst.sort()
        self.assertTrue(all((not hasattr(x, 'model') for x in lst[:2])))
        self.assertTrue(all((hasattr(x, 'model') for x in lst[2:])))

    def test_multiple_insertions_preserve_no_model_first_order(self):
        c = 100007
        f_model = self._make_bound(Foo, c)
        f_no1 = self._make_unbound(c)
        f_no2 = self._make_unbound(c)
        lst = [f_model]
        bisect.insort(lst, f_no1)
        bisect.insort(lst, f_no2)
        self.assertEqual(lst[:2], [f_no1, f_no2])
        self.assertEqual(lst[-1], f_model)

    def test_mixed_initial_ordering_sorted_result_consistent(self):
        c = 100008
        f_a = self._make_bound(Foo, c)
        f_b = self._make_bound(Bar, c)
        f_x = self._make_unbound(c)
        f_y = self._make_unbound(c)
        for initial in ([f_a, f_x, f_b, f_y], [f_x, f_a, f_y, f_b], [f_b, f_y, f_x, f_a]):
            sorted_list = sorted(initial)
            first_bound_index = next((i for i, v in enumerate(sorted_list) if hasattr(v, 'model')), None)
            if first_bound_index is None:
                continue
            self.assertTrue(all((not hasattr(v, 'model') for v in sorted_list[:first_bound_index])))
            self.assertTrue(all((hasattr(v, 'model') for v in sorted_list[first_bound_index:])))

from types import SimpleNamespace
from django.test import SimpleTestCase
from django.db import models

def make_dummy_model(app_label, model_name):
    """
    Return a simple dummy model-like object with a _meta attribute that
    contains app_label and model_name used by Field ordering/hash logic.
    """
    meta = SimpleNamespace(app_label=app_label, model_name=model_name, object_name=model_name)

    class Dummy:
        pass
    Dummy._meta = meta
    return Dummy

from django.db import models
from django.test import SimpleTestCase

def make_dummy_model(app_label, object_name):
    """
    Create a minimal dummy model-like object with a _meta that exposes
    app_label, model_name and label attributes to mimic real Django models'
    _meta interface used by Field.__lt__ and __hash__.
    """
    Meta = type('Meta', (), {})()
    Meta.app_label = app_label
    Meta.model_name = object_name.lower()
    Meta.label = f'{app_label}.{object_name}'
    Dummy = type(object_name, (), {'_meta': Meta})
    return Dummy

from django.test import SimpleTestCase
from django.db import models

class FieldComparisonRegressionTests(SimpleTestCase):

    def test_no_model_field_is_ordered_before_model_field_when_counters_equal(self):
        counter = 42
        no_model = self.make_field(counter, attach_model=None)
        stub_model = self.make_stub_model('app', 'mymodel')
        model_field = self.make_field(counter, attach_model=stub_model)
        self.assertTrue(no_model < model_field)
        self.assertFalse(model_field < no_model)

    def test_model_field_is_greater_than_no_model_field_when_counters_equal(self):
        counter = 100
        no_model = self.make_field(counter, attach_model=None)
        stub_model = self.make_stub_model('x', 'other')
        model_field = self.make_field(counter, attach_model=stub_model)
        self.assertTrue(model_field > no_model)
        self.assertFalse(no_model > model_field)

    def test_model_ordering_uses_app_label_and_model_name_tuple(self):
        m1 = self.make_stub_model('a', 'zname', label='z')
        m2 = self.make_stub_model('b', 'aname', label='a')
        counter = 999
        f1 = self.make_field(counter, attach_model=m1)
        f2 = self.make_field(counter, attach_model=m2)
        self.assertTrue(f1 < f2)
        self.assertFalse(f2 < f1)

    def test_sorting_mixed_fields_puts_no_model_first_then_models_by_meta(self):
        counter = 555
        no_model = self.make_field(counter, attach_model=None)
        m_a = self.make_stub_model('a', 'one')
        m_b = self.make_stub_model('a', 'two')
        field_a = self.make_field(counter, attach_model=m_b)
        field_b = self.make_field(counter, attach_model=m_a)
        lst = [field_a, no_model, field_b]
        lst.sort()
        self.assertEqual(lst, [no_model, field_b, field_a])