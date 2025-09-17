from sympy import symbols, Rational
from sympy.solvers.diophantine import diophantine
from sympy.utilities.iterables import signed_permutations
a, b, c, d, e, x, y, z = symbols('a b c d e x y z', integer=True)