from sympy import symbols, Integer
from sympy.tensor import IndexedBase
from sympy.matrices import MatrixSymbol
from sympy.printing.pycode import pycode, PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy import symbols, Integer
from sympy.tensor import IndexedBase
from sympy.matrices import MatrixSymbol
from sympy.printing.pycode import pycode, PythonCodePrinter, NumPyPrinter, MpmathPrinter
a, b, i = symbols('a b i')
p = IndexedBase('p')
M = MatrixSymbol('M', 3, 3)