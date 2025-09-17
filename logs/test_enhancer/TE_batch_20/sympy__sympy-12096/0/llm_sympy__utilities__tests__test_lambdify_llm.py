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