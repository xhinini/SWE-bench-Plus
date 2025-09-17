from __future__ import absolute_import
from sympy.core import symbols, Rational
from sympy.matrices import MatrixSymbol
from sympy.tensor import IndexedBase, Idx
from sympy.functions import acos
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, SciPyPrinter, pycode
x, y, i, j = symbols('x y i j')
p = IndexedBase('p')
A = MatrixSymbol('A', 2, 2)