from sympy import symbols, acos, pi
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
x, y = symbols('x y')
p = IndexedBase('p')