import builtins
from sympy import symbols, Symbol, Abs
from sympy.printing import srepr
x, y, z = symbols('x y z')
ENV = {}
exec('from sympy import *', ENV)