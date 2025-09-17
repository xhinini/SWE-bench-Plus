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

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import collections.abc
from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import collections.abc

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add_during_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        first = next(it)
        self.assertEqual(first, 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove_during_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_clear_during_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_direct_dict_setitem_during_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_multiple_iterators_raise_on_mutation(self):
        s = OrderedSet([1, 2, 3])
        it1 = reversed(s)
        it2 = reversed(s)
        self.assertEqual(next(it1), 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

    def test_reversed_partial_consumption_then_mutate_raises(self):
        s = OrderedSet([1, 2, 3, 5])
        it = reversed(s)
        self.assertEqual(next(it), 5)
        self.assertEqual(next(it), 3)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet


class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_returns_dict_reverseiterator_type(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        # Ensure the reverse iterator type matches reversing a plain dict,
        # i.e. it's a dict reverse iterator rather than a list reverse iterator.
        self.assertEqual(type(rev), type(reversed({})))

    def test_reversed_raises_runtimeerror_on_add(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate by adding a new key
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_remove(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate by removing an existing key
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_del_item_via_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via deletion
        del s.dict[1]
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_pop(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via pop
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_update(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via update
        s.dict.update({4: None})
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_clear(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via clear
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_popitem(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via popitem
        s.dict.popitem()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_setdefault(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via setdefault (adds new key)
        s.dict.setdefault(4, None)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_runtimeerror_on_setitem(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate underlying dict via explicit setitem
        s.dict.__setitem__(5, None)
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetMutationTests(SimpleTestCase):

    def test_reversed_add_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_remove_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_discard_existing_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.discard(2)
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_direct_assignment_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_clear_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_multiple_iterators_all_raise_on_change(self):
        s = OrderedSet([1, 2, 3])
        r1 = reversed(s)
        r2 = reversed(s)
        s.add(5)
        for r in (r1, r2):
            with self.assertRaises(RuntimeError):
                next(r)

    def test_reversed_partial_consumption_then_mutation_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        first = next(rev)
        self.assertEqual(first, 3)
        s.remove(1)
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_del_key_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        del s.dict[1]
        with self.assertRaises(RuntimeError):
            next(rev)

    def test_reversed_pop_key_raises(self):
        s = OrderedSet([1, 2, 3])
        rev = reversed(s)
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(rev)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):
    def test_reversed_raises_on_add(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.add(4)  # mutates underlying dict (size increases)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(2)  # mutates underlying dict (size decreases)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_clear(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.clear()  # direct dict mutation
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_setitem_new_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict[4] = None  # add new mapping entry
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_pop(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.pop(2)  # removes a key
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_popitem(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.popitem()  # mutates dict size
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_update_new_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.update({5: None})  # add new key via update
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_setdefault_new_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.setdefault(6, None)  # adds key when missing
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_del_key(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        del s.dict[1]  # delete key directly
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_multiple_mutations(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # multiple mutations before consuming iterator
        s.add(4)
        s.dict.pop(2)
        s.dict.update({7: None})
        with self.assertRaises(RuntimeError):
            # consume at least one element (should detect the change)
            next(it)

# No new imports required beyond those already present in the test module.
from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet


class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_iterator_raises_on_add_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate before consuming the iterator
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_add_after_partial_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        first = next(it)  # consume one element
        # Mutate after partial consumption
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_remove_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Remove an existing item before iterating
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_remove_after_partial_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        _ = next(it)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_internal_setitem_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate the underlying dict directly
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_internal_del_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Delete directly from the internal dict
        del s.dict[1]
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_internal_pop_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Pop an entry directly from the internal dict
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_on_internal_clear_before_iteration(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Clear the internal dict
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_when_mutated_between_multiple_iterators(self):
        s = OrderedSet([1, 2, 3, 4])
        it1 = reversed(s)
        it2 = reversed(s)
        # Mutate the set; both iterators should observe concurrent modification
        s.add(5)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

    def test_reversed_iterator_partial_iteration_then_internal_mutation_raises(self):
        s = OrderedSet([1, 2, 3, 4])
        it = reversed(s)
        # consume two items
        _ = next(it)
        _ = next(it)
        # mutate underlying dict
        s.dict[99] = None
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet


class OrderedSetMutationTests(SimpleTestCase):
    def test_reversed_iterator_raises_when_adding_item(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # Mutate after creating the iterator
        s.add(4)
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_removing_item(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_discarding_existing_item(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # discard an existing item mutates the dict
        s.discard(3)
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_clearing_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # clear the underlying dict directly
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_partial_iteration_then_add_raises_on_next(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # consume one element successfully
        first = next(it)
        self.assertEqual(first, 3)
        # mutate and expect subsequent iteration to raise
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_partial_iteration_then_remove_raises_on_next(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # consume one element successfully
        self.assertEqual(next(it), 3)
        s.remove(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_iterator_raises_when_mutating_dict_directly_setitem(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # direct setitem on underlying dict mutates it
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_pop_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.pop(1)
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_update_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict.update({5: None})
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_iterator_raises_when_clear_underlying_dict_after_partial_iter(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        # consume a single element
        self.assertEqual(next(it), 3)
        # clear underlying dict and expect RuntimeError on further iteration
        s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_add_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_remove_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_del_via_dict_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        del s.dict[1]
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_setitem_via_dict_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_update_via_dict_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict.update({5: None})
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_pop_via_dict_after_start_raises(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_multiple_reversed_iterators_both_raise_after_mutation(self):
        s = OrderedSet([1, 2, 3])
        it1 = reversed(s)
        it2 = reversed(s)
        self.assertEqual(next(it1), 3)
        self.assertEqual(next(it2), 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

    def test_reversed_iteration_for_loop_raises_mid_iteration(self):
        s = OrderedSet([1, 2, 3, 4])
        it = reversed(s)
        self.assertEqual(next(it), 4)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            list(it)

from django.utils.datastructures import OrderedSet
import collections.abc

def _inject_and_get_reversed(s, fake_dict):
    """
    Helper: replace s.dict with fake_dict and return (list(reversed(s)), reversed(s))
    The second returned value is the actual iterator (not yet consumed).
    """
    s.dict = fake_dict
    it = reversed(s)
    return (list(it), it)

def test_reversed_uses_underlying_dict_reversed_integers():
    s = OrderedSet()
    fake = FakeDict([1, 2, 3], [99, 98, 97])
    result_list, _ = _inject_and_get_reversed(s, fake)
    assert result_list == [99, 98, 97]

def test_reversed_uses_underlying_dict_reversed_strings():
    s = OrderedSet()
    fake = FakeDict(['a', 'b', 'c'], ['X', 'Y', 'Z'])
    result_list, _ = _inject_and_get_reversed(s, fake)
    assert result_list == ['X', 'Y', 'Z']

def test_reversed_uses_underlying_dict_reversed_single_element():
    s = OrderedSet()
    fake = FakeDict(['only'], ['reversed-only'])
    result_list, _ = _inject_and_get_reversed(s, fake)
    assert result_list == ['reversed-only']

def test_reversed_uses_underlying_dict_reversed_empty():
    s = OrderedSet()
    fake = FakeDict([], [])
    result_list, _ = _inject_and_get_reversed(s, fake)
    assert result_list == []

def test_reversed_returns_iterator_from_underlying():
    s = OrderedSet()
    fake = FakeDictWithCustomIterator([1, 2, 3], ['A', 'B', 'C'])
    result_list, iterator_obj = _inject_and_get_reversed(s, fake)
    assert result_list == ['A', 'B', 'C']
    assert isinstance(iterator_obj, collections.abc.Iterator)
    assert isinstance(iterator_obj, CustomRevIterator)

def test_reversed_prefers_dict_reversed_over_keys_list_materialization():
    s = OrderedSet()
    keys = ['k1', 'k2', 'k3']
    fake = FakeDict(keys, ['R1', 'R2', 'R3'])
    assert list(reversed(list(fake.keys()))) == ['k3', 'k2', 'k1']
    assert list(reversed(fake)) == ['R1', 'R2', 'R3']
    result_list, _ = _inject_and_get_reversed(s, fake)
    assert result_list == ['R1', 'R2', 'R3']

def test_reversed_multiple_calls_still_uses_underlying():
    s = OrderedSet()
    fake = FakeDict([10, 20], ['X10', 'X20'])
    s.dict = fake
    first = list(reversed(s))
    second = list(reversed(s))
    assert first == ['X10', 'X20']
    assert second == ['X10', 'X20']

def test_reversed_reflects_underlying_dict_reversed_changes():
    s = OrderedSet()
    fake = FakeDict([1, 2], ['first'])
    s.dict = fake
    assert list(reversed(s)) == ['first']
    fake._rev_sequence[:] = ['second', 'second2']
    assert list(reversed(s)) == ['second', 'second2']

def test_reversed_is_iterator_for_custom_underlying_iterator():
    s = OrderedSet()
    fake = FakeDictWithCustomIterator(['a', 'b'], ['C', 'D'])
    s.dict = fake
    it = reversed(s)
    assert isinstance(it, collections.abc.Iterator)
    assert list(it) == ['C', 'D']

def test_reversed_prefers_custom_reversed_when_keys_disagree():
    s = OrderedSet()
    fake = FakeDict(['k1', 'k2', 'k3'], ['custom1', 'custom2'])
    s.dict = fake
    assert list(reversed(s)) == ['custom1', 'custom2']

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_direct_dict_update(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_after_partial_iteration_then_add(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        first = next(it)
        self.assertEqual(first, 3)
        s.add(5)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_after_partial_iteration_then_remove(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        first = next(it)
        self.assertEqual(first, 3)
        s.remove(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_multiple_iterators_raise_after_mutation(self):
        s = OrderedSet([1, 2, 3])
        it1 = reversed(s)
        it2 = reversed(s)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it1)
        with self.assertRaises(RuntimeError):
            next(it2)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add_after_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        with self.assertRaises(RuntimeError):
            s.add(4)
            next(it)

    def test_reversed_raises_on_add_before_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        with self.assertRaises(RuntimeError):
            s.add(4)
            next(it)

    def test_reversed_raises_on_remove_after_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        with self.assertRaises(RuntimeError):
            s.remove(1)
            next(it)

    def test_reversed_raises_on_remove_before_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        with self.assertRaises(RuntimeError):
            s.remove(2)
            next(it)

    def test_reversed_raises_on_discard_after_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        with self.assertRaises(RuntimeError):
            s.discard(2)
            next(it)

    def test_reversed_raises_on_discard_before_start(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        with self.assertRaises(RuntimeError):
            s.discard(2)
            next(it)

    def test_reversed_raises_in_for_loop_on_add(self):
        s = OrderedSet([1, 2, 3])
        with self.assertRaises(RuntimeError):
            for _ in reversed(s):
                s.add(4)

    def test_reversed_raises_when_internal_dict_modified(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        with self.assertRaises(RuntimeError):
            s.dict[4] = None
            next(it)

    def test_reversed_raises_on_clear_of_internal_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        with self.assertRaises(RuntimeError):
            s.dict.clear()
            next(it)

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import types
from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet
import types

class OrderedSetReversedRegressionTests(SimpleTestCase):

    def test_reversed_uses_mapping_reversed(self):

        class CustomDict(dict):

            def __reversed__(self):
                return iter(['a', 'b'])
        s = OrderedSet([1, 2, 3])
        s.dict = CustomDict.fromkeys([1, 2, 3])
        self.assertEqual(list(reversed(s)), ['a', 'b'])

    def test_reversed_prefers_custom_over_keys_list(self):

        class CustomDict(dict):

            def keys(self):
                return ['k1', 'k2']

            def __reversed__(self):
                return iter(['reversed'])
        s = OrderedSet([1, 2, 3])
        s.dict = CustomDict.fromkeys([1, 2, 3])
        self.assertEqual(list(reversed(s)), ['reversed'])

    def test_reversed_side_effect_flag(self):

        class CustomDict(dict):

            def __init__(self, *a, **k):
                super().__init__(*a, **k)
                self.called = False

            def __reversed__(self):
                self.called = True
                return iter([])
        s = OrderedSet()
        s.dict = CustomDict.fromkeys([])
        _ = reversed(s)
        self.assertTrue(s.dict.called)

    def test_reversed_generator_return(self):

        class CustomDict(dict):

            def __reversed__(self):

                def gen():
                    yield 10
                    yield 20
                return gen()
        s = OrderedSet([1])
        s.dict = CustomDict.fromkeys([1])
        it = reversed(s)
        self.assertIsInstance(it, types.GeneratorType)
        self.assertEqual(list(it), [10, 20])

    def test_reversed_propagates_exceptions_from_custom_reversed(self):

        class CustomDict(dict):

            def __reversed__(self):
                raise RuntimeError('boom')
        s = OrderedSet([1, 2])
        s.dict = CustomDict.fromkeys([1, 2])
        with self.assertRaises(RuntimeError):
            list(reversed(s))

    def test_reversed_returns_non_iterator_value_if_custom_returns_it(self):

        class CustomDict(dict):

            def __reversed__(self):
                return [7, 8]
        s = OrderedSet([1, 2])
        s.dict = CustomDict.fromkeys([1, 2])
        self.assertEqual(reversed(s), [7, 8])

    def test_reversed_detects_mutation_of_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            list(it)

    def test_reversed_custom_works_with_different_key_orders(self):

        class CustomDict(dict):

            def __reversed__(self):
                return iter(['z', 'y', 'x'])
        s = OrderedSet(['a', 'b', 'c'])
        s.dict = CustomDict.fromkeys(['a', 'b', 'c'])
        self.assertEqual(list(reversed(s)), ['z', 'y', 'x'])

    def test_reversed_called_even_when_keys_differ(self):

        class CustomDict(dict):

            def keys(self):
                return ['unexpected']

            def __reversed__(self):
                return iter(['prefer-reversed'])
        s = OrderedSet([1])
        s.dict = CustomDict.fromkeys([1])
        self.assertEqual(list(reversed(s)), ['prefer-reversed'])

from django.test import SimpleTestCase
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):

    def setUp(self):
        self.s = OrderedSet([1, 2, 3])

    def test_reversed_raises_on_add(self):
        it = reversed(self.s)
        next(it)
        self.s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove(self):
        it = reversed(self.s)
        next(it)
        self.s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_discard_existing(self):
        it = reversed(self.s)
        next(it)
        self.s.discard(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_dict_setitem(self):
        it = reversed(self.s)
        next(it)
        self.s.dict[99] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_dict_delitem(self):
        it = reversed(self.s)
        next(it)
        del self.s.dict[2]
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_dict_pop(self):
        it = reversed(self.s)
        next(it)
        self.s.dict.pop(1)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_dict_clear(self):
        it = reversed(self.s)
        next(it)
        self.s.dict.clear()
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_when_size_increases_via_multiple_adds(self):
        it = reversed(self.s)
        next(it)
        self.s.add(4)
        self.s.add(5)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_when_size_decreases_via_multiple_removes(self):
        it = reversed(self.s)
        next(it)
        self.s.remove(2)
        self.s.remove(3)
        with self.assertRaises(RuntimeError):
            next(it)

from django.test import SimpleTestCase
import collections.abc
from django.utils.datastructures import OrderedSet

class OrderedSetReversedMutationTests(SimpleTestCase):

    def test_reversed_raises_on_add_new(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.add(4)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_remove(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.remove(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_discard_existing(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.discard(2)
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_direct_dict_assignment(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict[4] = None
        with self.assertRaises(RuntimeError):
            next(it)

    def test_reversed_raises_on_pop_from_underlying_dict(self):
        s = OrderedSet([1, 2, 3])
        it = reversed(s)
        self.assertEqual(next(it), 3)
        s.dict.pop(2)
        with self.assertRaises(RuntimeError):
            next(it)