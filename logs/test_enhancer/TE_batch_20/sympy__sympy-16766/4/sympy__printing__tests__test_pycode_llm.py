from sympy import sin, acos, Rational
from sympy.tensor import Indexed
from __future__ import absolute_import
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, pycode
from sympy import symbols, acos, sin, Rational
from sympy.tensor import IndexedBase, Indexed
from sympy.matrices import MatrixSymbol
x, y = symbols('x y')
p = IndexedBase('p')
q = IndexedBase('q')