from __future__ import absolute_import
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, pycode
from sympy.tensor import IndexedBase
from sympy import symbols, Integer
p = IndexedBase('p')
x, y = symbols('x y')