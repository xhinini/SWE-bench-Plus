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