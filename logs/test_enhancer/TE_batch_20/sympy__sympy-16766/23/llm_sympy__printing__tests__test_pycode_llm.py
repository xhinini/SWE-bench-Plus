import io
import os
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy import symbols
from sympy.tensor import IndexedBase
from sympy.printing import pycode as pycode_module
import io
import os
x, y = symbols('x y')
p = IndexedBase('p')
q = IndexedBase('q')
r = IndexedBase('r')