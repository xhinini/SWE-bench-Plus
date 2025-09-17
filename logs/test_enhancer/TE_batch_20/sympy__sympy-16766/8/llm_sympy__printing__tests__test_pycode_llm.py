from __future__ import absolute_import
import sys
from sympy import symbols, Tuple, Integer, Rational
from sympy.tensor import IndexedBase, Indexed
from sympy.matrices import MatrixSymbol
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter
x, y, z = symbols('x y z')
p = IndexedBase('p')
q = IndexedBase('q')