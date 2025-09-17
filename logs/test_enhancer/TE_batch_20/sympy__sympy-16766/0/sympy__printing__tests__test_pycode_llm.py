from __future__ import absolute_import
from sympy import symbols
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, SymPyPrinter, pycode
x, y = symbols('x y')
p = IndexedBase('p')