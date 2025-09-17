from sympy.functions import acos, erf, sign
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, SciPyPrinter
from sympy import IndexedBase
from sympy import symbols
x, y = symbols('x y')
p = IndexedBase('p')