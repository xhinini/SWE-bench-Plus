import pytest
from sympy import symbols
from sympy.solvers.diophantine import diophantine
x, y = symbols('x y', integer=True)
a, b = symbols('a b', integer=True)
u, v, X, Y, Z = symbols('u v X Y Z', integer=True)