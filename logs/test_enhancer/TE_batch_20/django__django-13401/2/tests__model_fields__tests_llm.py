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