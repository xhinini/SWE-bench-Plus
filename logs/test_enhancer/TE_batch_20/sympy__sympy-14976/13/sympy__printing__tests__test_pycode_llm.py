from __future__ import absolute_import, division, print_function
from sympy import Rational, symbols, asin, log1p, sin, Tuple
from sympy.printing.pycode import MpmathPrinter
x = symbols('x')
p = MpmathPrinter()