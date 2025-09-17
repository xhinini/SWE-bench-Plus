from decimal import Decimal

from django.db import models
from django.test import TestCase


class DecimalFieldTupleConversionTests(TestCase):

    def test_to_python_accepts_simple_decimal_tuple(self):
        f = models.DecimalField()
        value = (0, (1, 2, 3), -3)
        self.assertEqual(f.to_python(value), Decimal('0.123'))

    def test_to_python_accepts_decimal_as_tuple(self):
        f = models.DecimalField()
        tup = Decimal('1.23').as_tuple()
        self.assertEqual(f.to_python(tup), Decimal('1.23'))

    def test_to_python_accepts_subclassed_tuple(self):
        class MyTuple(tuple):
            pass
        f = models.DecimalField()
        value = MyTuple((0, (4, 5, 6), -3))
        self.assertEqual(f.to_python(value), Decimal('0.456'))

    def test_to_python_accepts_negative_sign_tuple(self):
        f = models.DecimalField()
        value = (1, (1, 2), -2)
        self.assertEqual(f.to_python(value), Decimal('-0.12'))

    def test_to_python_accepts_zero_exponent_tuple(self):
        f = models.DecimalField()
        value = (0, (1, 2, 3), 0)
        self.assertEqual(f.to_python(value), Decimal('123'))

    def test_to_python_accepts_positive_exponent_tuple(self):
        f = models.DecimalField()
        value = (0, (1,), 5)
        self.assertEqual(f.to_python(value), Decimal('100000'))

    def test_to_python_accepts_negative_large_exponent_tuple(self):
        f = models.DecimalField()
        value = (0, (1,), -5)
        self.assertEqual(f.to_python(value), Decimal('0.00001'))

    def test_to_python_accepts_negative_decimal_as_tuple(self):
        f = models.DecimalField()
        tup = Decimal('-45.6').as_tuple()
        self.assertEqual(f.to_python(tup), Decimal('-45.6'))

    def test_to_python_accepts_zero_tuple(self):
        f = models.DecimalField()
        value = (0, (0,), 0)
        self.assertEqual(f.to_python(value), Decimal('0'))

    def test_to_python_accepts_various_digits_and_exponent(self):
        f = models.DecimalField()
        value = (0, (9, 8, 7), -1)
        self.assertEqual(f.to_python(value), Decimal('98.7'))

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase


class DecimalFieldTupleTests(TestCase):
    def setUp(self):
        # Use generous max_digits/decimal_places to avoid DecimalValidator errors
        self.field = models.DecimalField(max_digits=30, decimal_places=10)

    def test_to_python_accepts_decimal_tuple_basic(self):
        val = (0, (1, 2, 3), -2)  # represents Decimal('1.23')
        self.assertEqual(self.field.to_python(val), Decimal('1.23'))

    def test_to_python_accepts_decimal_tuple_negative(self):
        val = (1, (1, 2, 3), -2)  # represents Decimal('-1.23')
        self.assertEqual(self.field.to_python(val), Decimal('-1.23'))

    def test_to_python_accepts_decimal_tuple_zero(self):
        val = (0, (0,), 0)  # represents Decimal('0')
        self.assertEqual(self.field.to_python(val), Decimal('0'))

    def test_to_python_accepts_large_integer_tuple(self):
        val = (0, (1, 0, 0, 0, 0), 0)  # represents Decimal('10000')
        self.assertEqual(self.field.to_python(val), Decimal('10000'))

    def test_to_python_accepts_tuple_constructed_via_tuple_constructor(self):
        # Ensure a tuple produced via tuple(...) is accepted
        val = tuple([0, (7, 8), -1])  # represents Decimal('7.8')
        self.assertEqual(self.field.to_python(val), Decimal('7.8'))

    def test_to_python_accepts_subclass_of_tuple(self):
        class MyTuple(tuple):
            pass
        # Construct MyTuple from an iterable so the instance is a MyTuple
        val = MyTuple((0, (4, 5), -1))  # represents Decimal('4.5')
        # Confirm it's indeed an instance of tuple subclass
        self.assertIsInstance(val, tuple)
        self.assertNotEqual(type(val), tuple)
        # The DecimalField.to_python should accept it and return the appropriate Decimal
        self.assertEqual(self.field.to_python(val), Decimal('4.5'))

    def test_to_python_accepts_many_digits_tuple(self):
        val = (0, (9, 9, 9, 9), -3)  # represents Decimal('9.999')
        self.assertEqual(self.field.to_python(val), Decimal('9.999'))

    def test_clean_accepts_decimal_tuple(self):
        # full clean pipeline should accept the tuple form
        val = (0, (1, 2, 3), -2)
        self.assertEqual(self.field.clean(val, None), Decimal('1.23'))

    def test_get_prep_value_accepts_decimal_tuple(self):
        # get_prep_value calls to_python internally for DecimalField
        val = (0, (1, 2, 3), -2)
        self.assertEqual(self.field.get_prep_value(val), Decimal('1.23'))

    def test_to_python_accepts_decimal_as_tuple_from_decimal_as_tuple(self):
        # Decimal.as_tuple() returns a DecimalTuple (a tuple-like object)
        dec = Decimal('12.345')
        dec_tuple = dec.as_tuple()
        # Sanity: ensure it's tuple-like
        self.assertIsInstance(dec_tuple, tuple)
        # The field should accept this tuple representation and reconstruct the Decimal
        self.assertEqual(self.field.to_python(dec_tuple), Decimal('12.345'))

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import models

class DecimalFieldRegressionTests(TestCase):

    def setUp(self):
        self.field = models.DecimalField(max_digits=5, decimal_places=2)

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

class DecimalFieldRegressionTests(TestCase):

    def test_to_python_accepts_tuple_representation_simple(self):
        f = models.DecimalField()
        value = (0, (1,), -1)
        self.assertEqual(f.to_python(value), Decimal('0.1'))

    def test_to_python_accepts_tuple_multiple_digits(self):
        f = models.DecimalField()
        value = (0, (1, 2, 3), -3)
        self.assertEqual(f.to_python(value), Decimal('0.123'))

    def test_to_python_accepts_tuple_negative_sign(self):
        f = models.DecimalField()
        value = (1, (1,), -1)
        self.assertEqual(f.to_python(value), Decimal('-0.1'))

    def test_to_python_accepts_tuple_with_list_digits_inside(self):
        f = models.DecimalField()
        value = (0, [1, 2], -2)
        self.assertEqual(f.to_python(value), Decimal('0.12'))

    def test_clean_accepts_tuple_representation(self):
        f = models.DecimalField()
        value = (0, (4, 5), -2)
        cleaned = f.clean(value, None)
        self.assertEqual(cleaned, Decimal('0.45'))

from collections import namedtuple

def test_to_python_accepts_decimal_tuple_basic(self):
    f = models.DecimalField()
    val = (0, (1, 2), -1)
    self.assertEqual(f.to_python(val), Decimal('1.2'))

def test_clean_accepts_decimal_tuple_basic(self):
    f = models.DecimalField()
    val = (0, (1, 2), -1)
    self.assertEqual(f.clean(val, None), Decimal('1.2'))

def test_get_prep_value_accepts_decimal_tuple_basic(self):
    f = models.DecimalField()
    val = (0, (1, 2), -1)
    self.assertEqual(f.get_prep_value(val), Decimal('1.2'))

def test_to_python_accepts_decimal_tuple_subclass(self):

    class MyTuple(tuple):
        pass
    f = models.DecimalField()
    val = MyTuple((0, (4, 5), -1))
    self.assertEqual(f.to_python(val), Decimal('4.5'))

def test_clean_accepts_decimal_tuple_subclass(self):

    class MyTuple(tuple):
        pass
    f = models.DecimalField()
    val = MyTuple((0, (4, 5), -1))
    self.assertEqual(f.clean(val, None), Decimal('4.5'))

def test_get_prep_value_accepts_decimal_tuple_subclass(self):

    class MyTuple(tuple):
        pass
    f = models.DecimalField()
    val = MyTuple((0, (4, 5), -1))
    self.assertEqual(f.get_prep_value(val), Decimal('4.5'))

def test_to_python_accepts_namedtuple_decimal_representation(self):
    NT = namedtuple('NT', ('a', 'b', 'c'))
    f = models.DecimalField()
    val = NT(0, (7, 8), -1)
    self.assertEqual(f.to_python(val), Decimal('7.8'))

def test_clean_accepts_namedtuple_decimal_representation(self):
    NT = namedtuple('NT', ('a', 'b', 'c'))
    f = models.DecimalField()
    val = NT(0, (7, 8), -1)
    self.assertEqual(f.clean(val, None), Decimal('7.8'))

def test_get_db_prep_save_accepts_decimal_tuple(self):
    f = models.DecimalField(max_digits=3, decimal_places=1)
    val = (0, (4, 5), -1)
    expected = connection.ops.adapt_decimalfield_value(Decimal('4.5'), 3, 1)
    self.assertEqual(f.get_db_prep_save(val, connection), expected)

def test_get_db_prep_save_accepts_decimal_tuple_subclass(self):

    class MyTuple(tuple):
        pass
    f = models.DecimalField(max_digits=3, decimal_places=1)
    val = MyTuple((0, (4, 5), -1))
    expected = connection.ops.adapt_decimalfield_value(Decimal('4.5'), 3, 1)
    self.assertEqual(f.get_db_prep_save(val, connection), expected)

from decimal import Decimal
from collections import namedtuple
from django.test import TestCase
from django.db import models
from decimal import Decimal
from collections import namedtuple

from django.test import TestCase
from django.db import models

class DecimalFieldTupleTests(TestCase):
    def setUp(self):
        # Use high max_digits/decimal_places to avoid validator interference.
        self.field = models.DecimalField(max_digits=30, decimal_places=10)

    def test_to_python_tuple_basic(self):
        # (sign, digits, exponent) -> 1.23
        value = (0, (1, 2, 3), -2)
        self.assertEqual(self.field.to_python(value), Decimal('1.23'))

    def test_to_python_tuple_negative(self):
        # sign=1 -> negative value
        value = (1, (1, 2), -1)
        self.assertEqual(self.field.to_python(value), Decimal('-1.2'))

    def test_clean_accepts_tuple(self):
        # clean() wraps to_python + validate + run_validators; should return Decimal
        value = (0, (3, 0, 0), -2)  # 3.00
        cleaned = self.field.clean(value, None)
        self.assertEqual(cleaned, Decimal('3.00'))

    def test_get_prep_value_accepts_tuple(self):
        # get_prep_value delegates to to_python; should produce Decimal
        value = (0, (3,), -1)  # 0.3
        self.assertEqual(self.field.get_prep_value(value), Decimal('0.3'))

    def test_to_python_namedtuple(self):
        # A namedtuple is a subclass of tuple; Decimal should accept it.
        NT = namedtuple('NT', ('sign', 'digits', 'exponent'))
        value = NT(0, (4, 2), -1)  # 4.2
        self.assertEqual(self.field.to_python(value), Decimal('4.2'))

    def test_to_python_tuple_large_digits(self):
        value = (0, (0, 0, 1), -3)  # 0.001
        self.assertEqual(self.field.to_python(value), Decimal('0.001'))

    def test_to_python_tuple_zero_exponent(self):
        value = (0, (1, 0, 0), 0)  # 100
        self.assertEqual(self.field.to_python(value), Decimal('100'))

    def test_to_python_tuple_single_digit(self):
        value = (0, (7,), -1)  # 0.7
        self.assertEqual(self.field.to_python(value), Decimal('0.7'))

    def test_clean_tuple_preserves_scale(self):
        # Ensure scale/precision from tuple are preserved by to_python/clean
        value = (0, (8, 3, 2, 0), -3)  # 8.320
        cleaned = self.field.clean(value, None)
        self.assertEqual(cleaned, Decimal('8.320'))

    def test_to_python_tuple_many_digits(self):
        value = (0, (1,)*20, -10)  # 11111111111111111111 * 10^-10
        result = self.field.to_python(value)
        # construct expected Decimal from the tuple for clarity
        digits = ''.join('1' for _ in range(20))
        expected = Decimal(digits).scaleb(-10)
        self.assertEqual(result, expected)