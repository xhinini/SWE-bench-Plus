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

import mpmath
from decimal import Decimal
from fractions import Fraction
try:
    import numpy
except Exception:
    numpy = None
import mpmath
from decimal import Decimal
from fractions import Fraction
from sympy import Function, Float, Rational
from sympy.utilities.pytest import skip
try:
    import numpy as _numpy
    numpy = _numpy
except Exception:
    numpy = None
TOL = 1e-12

def test_evalf_imp_returns_mpmath_mpf_single():

    class MF(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(x))
    res = MF(0.2).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - float(mpmath.mpf('0.2'))) < TOL

def test_evalf_imp_returns_mpmath_mpf_two_args():

    class MF2(Function):

        @staticmethod
        def _imp_(x, y):
            return mpmath.mpf(str(x + y))
    res = MF2(0.1, 0.2).evalf(50)
    assert isinstance(res, Float)
    assert abs(float(res) - float(mpmath.mpf('0.30000000000000004'))) < TOL

def test_evalf_imp_returns_mpmath_mpf_from_rational_arg():

    class MF3(Function):

        @staticmethod
        def _imp_(x):
            return mpmath.mpf(str(x))
    res = MF3(Rational(1, 3)).evalf(40)
    assert isinstance(res, Float)
    assert abs(float(res) - float(mpmath.mpf(str(Rational(1, 3))))) < 1e-10

def test_evalf_imp_returns_decimal():

    class DF(Function):

        @staticmethod
        def _imp_(x):
            return Decimal(str(x))
    res = DF(0.125).evalf(30)
    assert isinstance(res, Float)
    assert abs(float(res) - float(Decimal('0.125'))) < TOL

import mpmath
from sympy import Float, Rational
from sympy.utilities.lambdify import implemented_function
import mpmath
from sympy import Float, Rational
from sympy.utilities.lambdify import implemented_function

def test_regression_evalf_impl_mpf_constant():
    f = implemented_function('f_const', lambda x: mpmath.mpf('1.234567890123456789'))
    v = f(0).evalf(20)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_uses_argument():
    f = implemented_function('f_usearg', lambda x: mpmath.mpf(str(float(x))) * mpmath.mpf('2'))
    v = f(1).evalf(15)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_multiple_args():

    def impl(x, y):
        return mpmath.mpf(str(float(x) + float(y)))
    g = implemented_function('g_multi', impl)
    v = g(1, 2).evalf(10)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_nested_calls():
    f_inner = implemented_function('f_inner', lambda x: mpmath.mpf('3.0'))
    f_outer = implemented_function('f_outer', lambda x: mpmath.mpf(str(float(x))) + mpmath.mpf('1.0'))
    expr = f_outer(f_inner(0))
    v = expr.evalf(12)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_with_rational_input():
    h = implemented_function('h_rat', lambda x: mpmath.mpf(str(float(x))) / mpmath.mpf('2'))
    v = h(Rational(1, 2)).evalf(20)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_precision_attribute():
    f = implemented_function('f_prec', lambda x: mpmath.mpf('0.125'))
    v = f(0).evalf(30)
    assert isinstance(v, Float)
    assert hasattr(v, '_prec')

def test_regression_evalf_impl_mpf_different_value():
    f = implemented_function('f_diff', lambda x: mpmath.mpf('42.4242'))
    v = f(10).evalf(15)
    assert isinstance(v, Float)

def test_regression_evalf_impl_mpf_many_args():

    def impl_many(a, b, c, d):
        return mpmath.mpf(str(float(a) + float(b) + float(c) + float(d)))
    ff = implemented_function('ff_many', impl_many)
    v = ff(1, 2, 3, 4).evalf(10)
    assert isinstance(v, Float)

import mpmath
from sympy import Function, Float, Rational, sqrt, sin, S
import mpmath
from sympy import Function, Float, Rational, sqrt, sin
from sympy import S

def test_evalf_wraps_mpmath_mpf_single_arg():

    class F(Function):

        def _imp_(self, x):
            return mpmath.mpf(str(float(x)))
    res = F(0.2).evalf(30)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

def test_evalf_wraps_mpmath_mpf_rational_arg():

    class F(Function):

        def _imp_(self, x):
            return mpmath.mpf(str(float(x)))
    res = F(Rational(1, 3)).evalf(40)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

def test_evalf_wraps_mpmath_mpf_sqrt_arg():

    class F(Function):

        def _imp_(self, x):
            return mpmath.mpf(str(float(x)))
    res = F(sqrt(2)).evalf(25)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

def test_evalf_wraps_mpmath_mpf_from_sympy_float_arg():

    class Ff(Function):

        def _imp_(self, x):
            return mpmath.mpf(str(float(x)))
    arg = Float('0.1234567890123456789012345', 50)
    res = Ff(arg).evalf(40)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

def test_evalf_wraps_mpmath_mpf_with_trigonometric_argument():

    class T(Function):

        def _imp_(self, x):
            return mpmath.mpf(str(float(x)))
    res = T(sin(0.2)).evalf(30)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

def test_evalf_wraps_mpmath_mpf_multi_eval_calls():

    class M(Function):

        def _imp_(self, x, y, z):
            return mpmath.mpf(str(float(x) + float(y) + float(z)))
    res = M(Rational(1, 10), sqrt(2), Float('0.3333333333333333', 30)).evalf(35)
    assert isinstance(res, Float)
    assert not _is_mpmath_number(res)

import mpmath
from sympy import Rational, Integer, Float
from sympy.utilities.lambdify import implemented_function
import mpmath
from sympy import Rational, Integer, Float
from sympy.utilities.lambdify import implemented_function

def test_impl_mpmath_mpf_direct():
    f = implemented_function('f_mpf_direct', lambda x: mpmath.mpf('0.125'))
    r = f(1).evalf(40)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.125) < 1e-25

def test_impl_mpmath_mpf_nested():
    f = implemented_function('f_mpf_nested', lambda x: mpmath.mpf('0.25'))
    r = f(f(1)).evalf(40)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.25) < 1e-25

def test_impl_mpmath_mpf_in_expression():
    f = implemented_function('f_mpf_expr', lambda x: mpmath.mpf('0.375'))
    r = (f(1) + 1).evalf(40)
    assert isinstance(r, Float)
    assert abs(float(r) - 1.375) < 1e-25

import mpmath
from sympy import Float
from sympy.utilities.lambdify import implemented_function
from sympy import S

def test_impl_returning_mpmath_mpf_is_wrapped_to_sympy_Float_type():
    f = implemented_function('f_mpf', lambda x: mpmath.mpf(str(float(x))))
    res = f(0.2).evalf(30)
    assert isinstance(res, Float), 'evalf should return a sympy.Float, got %r' % type(res)

def test_impl_returning_mpmath_mpf_value_matches_expected_precision():
    f = implemented_function('f_mpf_val', lambda x: mpmath.mpf(str(float(x))))
    prec = 40
    res = f(0.123456789).evalf(prec)
    expected_mpf = mpmath.mpf(str(float(0.123456789)))
    expected = Float(str(expected_mpf), prec)
    assert isinstance(res, Float)
    assert abs(res - expected) <= Float(1, prec) * Float('1e-10')

def test_impl_returning_mpmath_mpf_multi_argument():
    g = implemented_function('g_mpf', lambda x, y: mpmath.mpf(str(float(x) + float(y))))
    prec = 35
    res = g(0.1, 0.2).evalf(prec)
    assert isinstance(res, Float)
    expected = Float(str(mpmath.mpf(str(float(0.1 + 0.2)))), prec)
    assert abs(res - expected) <= Float(1, prec) * Float('1e-10')

def test_nested_implemented_functions_produce_sympy_Float():
    f = implemented_function('f_nested', lambda x: mpmath.mpf(str(float(x))))
    expr = f(f(0.2))
    res = expr.evalf(50)
    assert isinstance(res, Float)
    expected = Float(str(mpmath.mpf(str(float(0.2)))), 50)
    assert abs(res - expected) <= Float(1, 50) * Float('1e-10')

def test_impl_returning_mpmath_mpf_from_sympy_Float_argument():

    def _mk_mpf(x):
        return mpmath.mpf(str(float(x)))
    f = implemented_function('f_mpf_from_symfloat', _mk_mpf)
    prec = 25
    res = f(0.5).evalf(prec)
    assert isinstance(res, Float)
    expected = Float(str(mpmath.mpf(str(float(0.5)))), prec)
    assert abs(res - expected) <= Float(1, prec) * Float('1e-12')

import mpmath
from sympy import Function, Float, Rational
from math import isclose
import mpmath
from math import isclose
from sympy import Function, Float, Rational
from sympy.core.function import _coeff_isneg

def test_evalf_imp_returns_mpmath_mpf_single_arg():

    class F1(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf(str(x))
    res = F1(Float('0.2')).evalf(30)
    assert isinstance(res, Float)
    assert isclose(float(res), float(mpmath.mpf('0.2')), rel_tol=0, abs_tol=1e-18)

def test_evalf_imp_returns_mpmath_mpf_from_rational():

    class F2(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf(str(x))
    res = F2(Rational(1, 5)).evalf(40)
    assert isinstance(res, Float)
    assert isclose(float(res), float(mpmath.mpf('0.2')), rel_tol=0, abs_tol=1e-20)

def test_evalf_imp_multiple_args_sum_mpf():

    class F3(Function):

        @classmethod
        def _imp_(cls, a, b):
            return mpmath.mpf(str(a + b))
    res = F3(Float('1.2345'), Float('2.3456')).evalf(25)
    expected = mpmath.mpf('1.2345') + mpmath.mpf('2.3456')
    assert isinstance(res, Float)
    assert isclose(float(res), float(expected), rel_tol=0, abs_tol=1e-18)

def test_evalf_imp_negative_mpf():

    class F5(Function):

        @classmethod
        def _imp_(cls, x):
            return -mpmath.mpf(str(x))
    res = F5(Float('2.5')).evalf(20)
    assert isinstance(res, Float)
    assert isclose(float(res), float(-mpmath.mpf('2.5')), rel_tol=0, abs_tol=1e-18)

def test_evalf_imp_large_magnitude_mpf():

    class F6(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf(str(x)) * mpmath.mpf('1e20')
    res = F6(Float('1.23')).evalf(15)
    expected = mpmath.mpf('1.23') * mpmath.mpf('1e20')
    assert isinstance(res, Float)
    assert isclose(float(res), float(expected), rel_tol=0, abs_tol=100000.0)

def test_evalf_imp_respects_requested_precision_type():

    class F7(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf(str(x))
    res20 = F7(Float('0.3333333333333333')).evalf(20)
    res50 = F7(Float('0.3333333333333333')).evalf(50)
    assert isinstance(res20, Float) and isinstance(res50, Float)
    assert isclose(float(res20), float(mpmath.mpf('0.3333333333333333')), rel_tol=1e-12)
    assert isclose(float(res50), float(mpmath.mpf('0.3333333333333333')), rel_tol=1e-14)

def test_evalf_imp_arithmetic_inside_imp():

    class F8(Function):

        @classmethod
        def _imp_(cls, x, y, z):
            return mpmath.mpf(str(x)) * mpmath.mpf(str(y)) + mpmath.mpf(str(z))
    res = F8(Float('1.5'), Float('2.0'), Float('0.25')).evalf(30)
    expected = mpmath.mpf('1.5') * mpmath.mpf('2.0') + mpmath.mpf('0.25')
    assert isinstance(res, Float)
    assert isclose(float(res), float(expected), rel_tol=0, abs_tol=1e-16)

def test_evalf_imp_from_sympy_float_arg():

    class F9(Function):

        @classmethod
        def _imp_(cls, x):
            return mpmath.mpf(str(x))
    arg = Float('0.7071067811865476')
    res = F9(arg).evalf(35)
    assert isinstance(res, Float)
    assert isclose(float(res), float(mpmath.mpf(str(arg))), rel_tol=0, abs_tol=1e-18)

import mpmath
from decimal import Decimal
from fractions import Fraction
from sympy import Float
from sympy.utilities.lambdify import implemented_function
try:
    import numpy as _numpy
except Exception:
    _numpy = None
from sympy.utilities.pytest import skip
import mpmath
from decimal import Decimal
from fractions import Fraction
from sympy import Float
from sympy.utilities.lambdify import implemented_function
from sympy.utilities.pytest import skip
try:
    import numpy as _numpy
except Exception:
    _numpy = None

def test_evalf_imp_mpmath_mpf_single_arg():
    f = implemented_function('fm1', lambda x: mpmath.mpf(str(float(x))))
    r = f(0.2).evalf(30)
    assert isinstance(r, Float)
    assert abs(float(r) - 0.2) < 1e-25

def test_evalf_imp_mpmath_mpf_multiple_args():
    g = implemented_function('gm', lambda x, y: mpmath.mpf(str(float(x + y))))
    r = g(1, 2).evalf(30)
    assert isinstance(r, Float)
    assert float(r) == 3.0

def test_evalf_imp_decimal_return():
    d = implemented_function('hd', lambda x: Decimal('2.5'))
    r = d(1).evalf(20)
    assert isinstance(r, Float)
    assert float(r) == 2.5

def test_evalf_imp_mpmath_nested():
    f = implemented_function('fn', lambda x: mpmath.mpf(str(float(x))))
    r = f(f(2)).evalf(40)
    assert isinstance(r, Float)
    assert float(r) == 2.0

def test_evalf_imp_sum_mpmath_and_decimal():
    fm = implemented_function('fsm1', lambda x: mpmath.mpf(str(float(x))))
    fd = implemented_function('fsm2', lambda x: Decimal('1.0') * Decimal(str(float(x))))
    expr = fm(1) + fd(2)
    r = expr.evalf(30)
    assert isinstance(r, Float)
    assert abs(float(r) - 3.0) < 1e-25

import mpmath
from sympy import Float, Rational, S, Add
from sympy.utilities.lambdify import implemented_function

def test_evalf_wraps_mpmath_mpf_multiple_args():
    g = implemented_function('g_mpf_multi', lambda x, y: mpmath.mpf(str(x)) + mpmath.mpf(str(y)))
    res = g(1, 2).evalf(20)
    assert isinstance(res, Float)
    assert res == Float(3, 20)

def test_evalf_wraps_mpmath_mpf_nested():
    h = implemented_function('h_mpf_square', lambda x: mpmath.mpf(str(x)) ** 2)
    expr = h(h(2))
    res = expr.evalf(25)
    assert isinstance(res, Float)
    assert res == Float(16, 25)

def test_evalf_wraps_mpmath_mpf_rational_arg():
    k = implemented_function('k_mpf', lambda x: mpmath.mpf(str(x)) ** 2)
    res = k(Rational(1, 2)).evalf(18)
    assert isinstance(res, Float)
    assert res == Float('0.25', 18)

def test_evalf_in_expression_addition():
    addf = implemented_function('add_mpf', lambda x: mpmath.mpf(str(x)) * mpmath.mpf('0.5'))
    expr = Add(1, addf(1))
    res = expr.evalf(20)
    assert isinstance(res, Float)
    assert res == Float('1.5', 20)

def test_evalf_with_sympy_float_arg():
    ff = implemented_function('ff_mpf', lambda x: mpmath.mpf(str(x)) * mpmath.mpf('2'))
    arg = Float('0.125', 15)
    res = ff(arg).evalf(18)
    assert isinstance(res, Float)
    assert res == Float('0.25', 18)