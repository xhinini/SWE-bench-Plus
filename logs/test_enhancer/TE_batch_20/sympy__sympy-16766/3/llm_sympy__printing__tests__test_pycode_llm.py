from sympy import sin, IndexedBase, symbols, MatrixSymbol
from __future__ import absolute_import
import pytest
from sympy import symbols, IndexedBase, sin, cos, Symbol, Add
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, pycode
from sympy.matrices import MatrixSymbol
x, y = symbols('x y')
p = IndexedBase('p')