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