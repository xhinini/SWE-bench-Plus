import pytest
import mpmath
from sympy import Float, Rational
from sympy.utilities.lambdify import implemented_function
try:
    import numpy as _numpy
except Exception:
    _numpy = None