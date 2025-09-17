from __future__ import absolute_import
from sympy import symbols, acos
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter
x, y = symbols('x y')
p = IndexedBase('p')