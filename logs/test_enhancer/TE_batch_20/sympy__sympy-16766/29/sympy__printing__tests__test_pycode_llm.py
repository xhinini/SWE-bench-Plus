import inspect
from sympy import symbols, Integer
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter
from __future__ import absolute_import
import io
import os
import inspect
from sympy import symbols, Integer
from sympy.tensor import IndexedBase
import sympy.printing.pycode as pycode_module
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter
x, y = symbols('x y')
p = IndexedBase('p')