from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy.tensor import IndexedBase
from sympy import symbols
from sympy.matrices import MatrixSymbol
x, y = symbols('x y')
p = IndexedBase('p')