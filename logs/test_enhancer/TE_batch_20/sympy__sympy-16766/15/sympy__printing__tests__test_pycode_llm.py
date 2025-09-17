from sympy import sin, symbols
from sympy.tensor import IndexedBase
from sympy import symbols, sin
from sympy.tensor import IndexedBase
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter, SymPyPrinter, SciPyPrinter
x, y = symbols('x y')
p = IndexedBase('p')