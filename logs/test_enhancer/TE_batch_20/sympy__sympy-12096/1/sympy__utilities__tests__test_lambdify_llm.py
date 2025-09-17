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