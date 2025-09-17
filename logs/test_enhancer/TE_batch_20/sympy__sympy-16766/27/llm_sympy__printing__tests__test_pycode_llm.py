from sympy import Integer, Rational
from __future__ import absolute_import
from sympy.core import Expr, symbols, Rational
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, pycode
from sympy.functions import sign
from sympy import Integer
x, y, z = symbols('x y z')
p = IndexedBase('p')