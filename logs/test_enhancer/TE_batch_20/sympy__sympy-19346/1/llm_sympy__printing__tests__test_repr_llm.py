from sympy import Integer, symbols
from sympy.printing import srepr
import builtins
x, y = symbols('x y')
ENV = {}
exec('from sympy import *', ENV)