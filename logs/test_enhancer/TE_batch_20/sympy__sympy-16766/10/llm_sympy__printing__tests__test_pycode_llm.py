import inspect
from sympy import Integer
from __future__ import absolute_import
import inspect
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy.tensor import IndexedBase
from sympy import symbols, Integer
import sympy.printing.pycode as pycode_module
x, y, z = symbols('x y z')
p = IndexedBase('p')