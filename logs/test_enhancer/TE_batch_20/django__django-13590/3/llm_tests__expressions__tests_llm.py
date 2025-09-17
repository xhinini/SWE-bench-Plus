from django.test import TestCase
from django.db.models.sql.query import Query
from .models import Number

class ResolveLookupValueCustomSequenceTests(TestCase):

    def setUp(self):
        self.query = Number.objects.all().query

    def test_custom_tuple_subclass_two_args_with_make(self):

        class TwoArgTuple(tuple):
            _make = True

            def __new__(cls, a, b):
                return tuple.__new__(cls, (a, b))
        val = TwoArgTuple(1, 2)
        self._run_and_assert(val)

    def test_custom_tuple_subclass_three_args_with_make(self):

        class ThreeArgTuple(tuple):
            _make = True

            def __new__(cls, a, b, c):
                return tuple.__new__(cls, (a, b, c))
        val = ThreeArgTuple(1, 2, 3)
        self._run_and_assert(val)

    def test_custom_tuple_subclass_single_arg_with_make(self):

        class OneArgTuple(tuple):
            _make = True

            def __new__(cls, a):
                return tuple.__new__(cls, (a,))
        val = OneArgTuple(42)
        self._run_and_assert(val)

    def test_custom_tuple_subclass_four_args_with_make(self):

        class FourArgTuple(tuple):
            _make = True

            def __new__(cls, a, b, c, d):
                return tuple.__new__(cls, (a, b, c, d))
        val = FourArgTuple(1, 2, 3, 4)
        self._run_and_assert(val)

    def test_custom_tuple_subclass_five_args_with_make(self):

        class FiveArgTuple(tuple):
            _make = True

            def __new__(cls, a, b, c, d, e):
                return tuple.__new__(cls, (a, b, c, d, e))
        val = FiveArgTuple(9, 8, 7, 6, 5)
        self._run_and_assert(val)

    def test_custom_list_subclass_two_args_with_make(self):

        class TwoArgList(list):
            _make = True

            def __init__(self, a, b):
                super().__init__((a, b))
        val = TwoArgList(10, 20)
        self._run_and_assert(val)

    def test_custom_list_subclass_three_args_with_make(self):

        class ThreeArgList(list):
            _make = True

            def __init__(self, a, b, c):
                super().__init__((a, b, c))
        val = ThreeArgList(1, 2, 3)
        self._run_and_assert(val)

    def test_custom_list_subclass_single_arg_with_make(self):

        class OneArgList(list):
            _make = True

            def __init__(self, a):
                super().__init__((a,))
        val = OneArgList(7)
        self._run_and_assert(val)

    def test_custom_list_subclass_four_args_with_make(self):

        class FourArgList(list):
            _make = True

            def __init__(self, a, b, c, d):
                super().__init__((a, b, c, d))
        val = FourArgList(4, 3, 2, 1)
        self._run_and_assert(val)

    def test_custom_list_subclass_five_args_with_make(self):

        class FiveArgList(list):
            _make = True

            def __init__(self, a, b, c, d, e):
                super().__init__((a, b, c, d, e))
        val = FiveArgList(5, 4, 3, 2, 1)
        self._run_and_assert(val)