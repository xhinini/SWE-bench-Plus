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

from typing import NamedTuple as TypingNamedTuple
from collections import namedtuple
from typing import NamedTuple as TypingNamedTuple
from django.test import TestCase
from .models import Company

class ResolveLookupValueIterableTests(TestCase):

    def setUp(self):
        self.query = Company.objects.all().query

from typing import NamedTuple as TypingNamedTuple
from collections import namedtuple as collections_namedtuple
from typing import NamedTuple as TypingNamedTuple
from collections import namedtuple as collections_namedtuple
from django.test import TestCase
from .models import Company

class ResolveLookupValueIterableTests(TestCase):

    def setUp(self):
        self.query = Company.objects.all().query

    def test_custom_tuple_like_with_fields_attribute_constructs_from_single_iterable(self):

        class Weird(tuple):
            _fields = ('a', 'b')

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = Weird([7, 8])
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, Weird([7, 8]))

    def test_custom_tuple_like_with_three_elements(self):

        class Weird3(tuple):
            _fields = ('x', 'y', 'z')

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = Weird3([1, 2, 3])
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, Weird3([1, 2, 3]))

    def test_custom_tuple_like_with_nested_values(self):

        class WeirdNested(tuple):
            _fields = ('p', 'q')

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = WeirdNested([1, (2, 3)])
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, WeirdNested([1, (2, 3)]))

    def test_custom_tuple_like_with_expression_values(self):

        class WeirdExpr(tuple):
            _fields = ('a', 'b')

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = WeirdExpr([10, 20])
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, WeirdExpr([10, 20]))

    def test_custom_tuple_like_single_element(self):

        class WeirdSingle(tuple):
            _fields = ('only',)

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = WeirdSingle([42])
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, WeirdSingle([42]))

    def test_custom_tuple_like_with_large_number_of_elements(self):

        class WeirdMany(tuple):
            _fields = tuple(('f%d' % i for i in range(10)))

            def __new__(cls, iterable):
                return tuple.__new__(cls, iterable)
        value = WeirdMany(list(range(10)))
        resolved = self.query.resolve_lookup_value(value, None, True)
        self.assertEqual(resolved, WeirdMany(list(range(10))))

from typing import NamedTuple
from collections import namedtuple
from typing import NamedTuple as TypingNamedTuple
from django.test import TestCase
from django.db.models import F
from .models import Company

class ResolveLookupValueSequenceTests(TestCase):

    def setUp(self):
        self.query = Company.objects.all().query

from collections import namedtuple
from typing import NamedTuple as TypingNamedTuple
from django.test import TestCase
from django.db.models import F
from .models import Company

class ResolveLookupValueExtraTests(TestCase):

    def setUp(self):
        self.query = Company.objects.all().query

    def test_custom_tuple_with__fields_attribute(self):

        class FakeNamed(tuple):
            _fields = ('a', 'b')
        value = FakeNamed((1, 2))
        res = self.query.resolve_lookup_value(value, can_reuse=None, allow_joins=True)
        self.assertIsInstance(res, FakeNamed)
        self.assertEqual(tuple(res), (1, 2))