from __future__ import absolute_import, division, print_function
from sympy import Rational, Float, symbols
from sympy.functions import sign
from sympy.printing.pycode import MpmathPrinter
from sympy.utilities.pytest import raises
x = symbols('x')