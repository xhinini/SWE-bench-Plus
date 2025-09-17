from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReverseMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add_new_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove_existing_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_multiple_adds(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.add(4)
        s.add(5)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_when_underlying_dict_cleared(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_setitem_new_key_in_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_raises_on_add_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_raises_on_add_after_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_raises_on_remove_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_raises_on_remove_after_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.remove(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_raises_when_all_elements_removed_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(1)
        s.remove(2)
        s.remove(3)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_multiple_iterators_raise_on_mutation(self):
        s = OrderedSet([1, 2, 3])
        it1 = reversed(s)
        it2 = reversed(s)
        s.add(99)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

    def test_empty_iterator_raises_on_late_add(self):
        s = OrderedSet()
        it = reversed(s)
        s.add(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_partial_consumption_then_remove_raises(self):
        s = OrderedSet([1, 2, 3, 4])
        it = reversed(s)
        self.assertEqual(next(it), 4)
        self.assertEqual(next(it), 3)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import collections.abc

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_discard_existing_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.discard(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_add_after_some_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        first = next(it)
        self.assertEqual(first, 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove_after_some_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.remove(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_for_loop_raises_on_mutation(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        with self.assertRaises(RuntimeError):
            for i in it:
                s.add(4)
                pass

    def test_reversed_multiple_iterators_invalidated_on_mutation(self):
        s = OrderedSet([1, 2, 3])
        it1 = reversed(s)
        it2 = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

    def test_reversed_raises_on_direct_internal_dict_mutation(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import collections.abc

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_add_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_remove_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_direct_dict_setitem_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_dict_clear_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_dict_pop_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_update_via_dict_update_while_iterating_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        next(it)
        s.dict.update({5: None})
        with self.assertRaises(RuntimeError):
            next(it)