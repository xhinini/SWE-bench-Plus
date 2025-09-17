from sympy import symbols
from sympy.matrices import MatrixSymbol
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy.tensor import IndexedBase
from sympy import symbols
from sympy.matrices import MatrixSymbol
from sympy.printing.pycode import PythonCodePrinter, NumPyPrinter, MpmathPrinter
from sympy.tensor import IndexedBase
x, y, z = symbols('x y z')
p = IndexedBase('p')
q = IndexedBase('q')