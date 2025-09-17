from sympy.printing.pycode import MpmathPrinter
from sympy.core import Rational
import sys

def test_mpmath_rational_basic():
    s = _doprint_without_int_print(Rational(1, 2))
    assert s == 'mpmath.mpf(1)/mpmath.mpf(2)'

def test_mpmath_rational_negative_numerator():
    s = _doprint_without_int_print(Rational(-3, 4))
    assert s == 'mpmath.mpf(-3)/mpmath.mpf(4)'

def test_mpmath_rational_negative_denominator():
    s = _doprint_without_int_print(Rational(3, -4))
    assert s == 'mpmath.mpf(-3)/mpmath.mpf(4)'

def test_mpmath_rational_huge_integers():
    a = 123456789012345678901234567890
    b = 98765432109876543210
    s = _doprint_without_int_print(Rational(a, b))
    assert s == 'mpmath.mpf(%d)/mpmath.mpf(%d)' % (Rational(a, b).p, Rational(a, b).q)

def test_mpmath_rational_simplified_input():
    s = _doprint_without_int_print(Rational(5, 10))
    assert s == 'mpmath.mpf(1)/mpmath.mpf(2)'