from sympy import symbols
from sympy.solvers.diophantine import diophantine
x, y = symbols('x y', integer=True)
n, m = symbols('n m', integer=True)
expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}