import mpmath
from sympy import Function, Float, Integer, Rational
import mpmath
from sympy import Function, Float, Integer, Rational

def test_evalf_wraps_mpmath_mpf_return():

    class FM(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf('0.25')
    r = FM(1).evalf(50)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.25) < 1e-40

def test_evalf_wraps_mpmath_mpf_return_high_precision():

    class FM2(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf('0.123456789123456789123456789')
    r = FM2(1).evalf(60)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.12345678912345678) < 1e-30

import mpmath
from decimal import Decimal
from sympy import Float, symbols
from sympy.utilities.lambdify import implemented_function
import mpmath
from decimal import Decimal
from sympy import Float, symbols
from sympy.utilities.lambdify import implemented_function
x, y = symbols('x y')

def test_imp_returns_mpmath_mpf_converted_to_sympy_float():
    mpmath.mp.dps = 80
    f_mpf = implemented_function('imp_mpf', lambda z: mpmath.mpf('0.987654321234567890123456789'))
    e = f_mpf(1)
    r = e.evalf(50)
    assert isinstance(r, Float)
    s_low = str(e.evalf(10))
    s_high = str(e.evalf(50))
    assert s_high != s_low
    assert len(s_high) > len(s_low)

def test_imp_returns_decimal_converted_to_sympy_float():
    f_dec = implemented_function('imp_dec', lambda z: Decimal('0.3141592653589793238462643383279'))
    e = f_dec(1)
    r = e.evalf(30)
    assert isinstance(r, Float)
    s_low = str(e.evalf(8))
    s_high = str(e.evalf(30))
    assert s_high != s_low
    assert len(s_high) > len(s_low)

def test_imp_mpf_multiarg_sum_and_precision():
    mpmath.mp.dps = 60
    f_sum = implemented_function('imp_sum', lambda a, b: mpmath.mpf(str(a)) + mpmath.mpf(str(b)))
    e = f_sum(1, 2)
    r = e.evalf(35)
    assert isinstance(r, Float)
    assert abs(float(r) - 3.0) < 1e-12
    assert len(str(e.evalf(10))) < len(str(e.evalf(35)))

def test_imp_decimal_multiargs_produces_sympy_float():
    f_dec2 = implemented_function('imp_dec2', lambda a, b: Decimal('1.111111111111111111') * (Decimal(str(a)) + Decimal(str(b))))
    e = f_dec2(2, 3)
    r = e.evalf(25)
    assert isinstance(r, Float)
    assert abs(float(r) - float(Decimal('1.111111111111111111') * Decimal(5))) < 1e-12

def test_imp_mpf_not_returned_raw_type():
    mpmath.mp.dps = 50
    f_mpf2 = implemented_function('imp_mpf2', lambda z: mpmath.mpf('0.111111111111111111111111111111'))
    e = f_mpf2(1)
    r = e.evalf(20)
    assert isinstance(r, Float)

def test_imp_decimal_not_returned_raw_decimal():
    f_dec3 = implemented_function('imp_dec3', lambda z: Decimal('0.22222222222222222222222222'))
    e = f_dec3(1)
    r = e.evalf(18)
    assert isinstance(r, Float)

import mpmath
from sympy import Float, Rational
from sympy.utilities.lambdify import implemented_function

def test_impl_mpf_single_arg():
    f = implemented_function('f_mpf_1', lambda x: mpmath.mpf(x) ** 2)
    r = f(2).evalf(20)
    assert isinstance(r, Float)
    assert r == Float(4)

def test_impl_mpf_nested():
    f = implemented_function('f_mpf_2', lambda x: mpmath.mpf(x) ** 2)
    r = f(f(2)).evalf(30)
    assert isinstance(r, Float)
    assert r == Float(16)

def test_impl_mpf_two_args():
    g = implemented_function('g_mpf_1', lambda x, y: mpmath.mpf(x) + mpmath.mpf(y))
    r = g(1, 3).evalf()
    assert isinstance(r, Float)
    assert r == Float(4)

def test_impl_mpf_rational_arg():
    h = implemented_function('h_mpf_1', lambda x: mpmath.mpf(x) * 2)
    r = h(Rational(1, 2)).evalf(25)
    assert isinstance(r, Float)
    assert r == Float(1)

def test_impl_mpf_mpf_input():
    k = implemented_function('k_mpf_1', lambda x: mpmath.mpf(x) ** 3)
    inp = mpmath.mpf('1.5')
    r = k(inp).evalf(20)
    assert isinstance(r, Float)
    assert r == Float(inp ** 3)

def test_impl_mpf_precision_preserved_numeric_value():
    f = implemented_function('f_mpf_3', lambda x: mpmath.mpf(x) / 3)
    r20 = f(2).evalf(20)
    r50 = f(2).evalf(50)
    assert isinstance(r20, Float) and isinstance(r50, Float)
    assert float(r20) == float(r50) == float(mpmath.mpf(2) / 3)

def test_impl_mpf_nested_mixed():
    f = implemented_function('f_mpf_4', lambda x: mpmath.mpf(x) + 1)
    g = implemented_function('g_mpf_2', lambda x: mpmath.mpf(x) * 2)
    r = g(f(2)).evalf(30)
    assert isinstance(r, Float)
    assert r == Float((mpmath.mpf(2) + 1) * 2)

def test_impl_mpf_multiple_evalf_calls():
    f = implemented_function('f_mpf_5', lambda x: mpmath.mpf(x) ** 2 + mpmath.mpf('0.25'))
    a = f(3)
    r1 = a.evalf(15)
    r2 = a.evalf(30)
    assert isinstance(r1, Float) and isinstance(r2, Float)
    assert r1 == Float(9.25) and r2 == Float(9.25)

def test_impl_mpf_non_integer_args():
    f = implemented_function('f_mpf_6', lambda x: mpmath.mpf(x) * mpmath.mpf('0.1'))
    r = f(Rational(3, 2)).evalf(20)
    assert isinstance(r, Float)
    assert r == Float(mpmath.mpf(Rational(3, 2)) * mpmath.mpf('0.1'))

import mpmath
from sympy import Function, Integer, Rational, Float
from sympy import Function, Integer, Rational, Float
import mpmath

def test_evalf_imp_returns_mpmath_mpf():

    class FM(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf('0.125')
    r = FM(2).evalf(40)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.125) < 1e-20

def test_evalf_imp_mpmath_using_args_ignored():

    class FM2(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf('3.14159')
    r = FM2(1).evalf(30)
    assert isinstance(r, Float)
    assert abs(float(r) - 3.14159) < 1e-12

import mpmath
from sympy.utilities.pytest import skip
from sympy import Function, Float, Rational

def test_evalf_with_imp_returning_mpmath_mpf_single_arg():
    if not mpmath:
        skip('mpmath not installed')

    class F_single(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) + mpmath.mpf('0.5')
    res = F_single(2).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - 2.5) < 1e-12

def test_evalf_with_imp_returning_mpmath_mpf_two_args():
    if not mpmath:
        skip('mpmath not installed')

    class F_two(Function):

        @staticmethod
        def _imp_(x, y):
            return mpmath.mpf(str(float(x))) * mpmath.mpf(str(float(y)))
    res = F_two(3, 4).evalf(40)
    assert isinstance(res, Float)
    assert abs(float(res) - 12.0) < 1e-12

def test_evalf_with_imp_returning_mpmath_mpf_three_args():
    if not mpmath:
        skip('mpmath not installed')

    class F_three(Function):

        @staticmethod
        def _imp_(a, b, c):
            s = float(a) + float(b) + float(c)
            return mpmath.mpf(str(s))
    res = F_three(1, 2, 3).evalf(20)
    assert isinstance(res, Float)
    assert abs(float(res) - 6.0) < 1e-12

def test_evalf_with_imp_and_rational_argument():
    if not mpmath:
        skip('mpmath not installed')

    class F_rat(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) / mpmath.mpf('2')
    res = F_rat(Rational(3, 2)).evalf(25)
    assert isinstance(res, Float)
    assert abs(float(res) - 0.75) < 1e-12

def test_evalf_with_imp_when_args_are_already_floats():
    if not mpmath:
        skip('mpmath not installed')

    class F_already_float(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) * mpmath.mpf('1.25')
    res = F_already_float(Float('2.0')).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - 2.5) < 1e-12

def test_evalf_with_imp_multiple_calls_consistent_behavior():
    if not mpmath:
        skip('mpmath not installed')

    class F_consistent(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) + mpmath.mpf('1.0')
    for v, expected in [(0, 1.0), (1, 2.0), (2.5, 3.5)]:
        res = F_consistent(v).evalf(20)
        assert isinstance(res, Float)
        assert abs(float(res) - expected) < 1e-12

def test_evalf_with_imp_high_precision():
    if not mpmath:
        skip('mpmath not installed')

    class F_highp(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) + mpmath.mpf('0.125')
    res = F_highp(8).evalf(80)
    assert isinstance(res, Float)
    assert abs(float(res) - 8.125) < 1e-12

def test_evalf_with_imp_and_mixed_argument_types():
    if not mpmath:
        skip('mpmath not installed')

    class F_mixed(Function):

        @staticmethod
        def _imp_(x, y):
            return mpmath.mpf(str(float(x))) + mpmath.mpf(str(float(y)))
    res = F_mixed(1, Rational(1, 2)).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - 1.5) < 1e-12

def test_evalf_with_imp_nested_function_calls():
    if not mpmath:
        skip('mpmath not installed')

    class Inner(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) * mpmath.mpf('2')

    class Outer(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(float(x))) + mpmath.mpf('1')
    inner = Inner(3).evalf(30)
    res = Outer(inner).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - 7.0) < 1e-12