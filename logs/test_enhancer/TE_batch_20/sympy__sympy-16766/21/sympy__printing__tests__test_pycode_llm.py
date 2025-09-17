from sympy import symbols, Rational
from sympy.core.numbers import pi
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from __future__ import absolute_import
from sympy import symbols, Rational
from sympy.core.numbers import pi
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
x, y = symbols('x y')
p = IndexedBase('p')
q = IndexedBase('q')