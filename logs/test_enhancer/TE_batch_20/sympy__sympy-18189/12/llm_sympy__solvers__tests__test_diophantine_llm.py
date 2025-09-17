from sympy.utilities import default_sort_key
from sympy import symbols
from sympy import symbols
from sympy.utilities import default_sort_key
from sympy.solvers.diophantine import diophantine
n, m = symbols('n m', integer=True)
eq1 = n ** 4 + m ** 4 - 2 ** 4 - 3 ** 4
assert diophantine(eq1, syms=(m, n), permute=True) == _expected_for_swapped(eq1, (m, n))
x, y = symbols('x y', integer=True)
eq2 = x - 3 * y + 2
assert diophantine(eq2, syms=[y, x], permute=True) == _expected_for_swapped(eq2, (y, x))
x, y, z = symbols('x y z', integer=True)
eq3 = 4 * x + 3 * y - 4 * z + 5
assert diophantine(eq3, syms=(z, x, y), permute=True) == _expected_for_swapped(eq3, (z, x, y))
a, b, c = symbols('a b c', integer=True)
eq4 = a ** 2 + b ** 2 + c ** 2 - 14
assert diophantine(eq4, syms=(c, b, a), permute=True) == _expected_for_swapped(eq4, (c, b, a))
p, q = symbols('p q', integer=True)
eq5 = p ** 4 + q ** 4 - 2 ** 4 - 3 ** 4
assert diophantine(eq5, syms=(q, p), permute=True) == _expected_for_swapped(eq5, (q, p))
x, y, z = symbols('x y z', integer=True)
eq6 = 2 * x ** 2 + y ** 2 - 2 * z ** 2
assert diophantine(eq6, syms=(z, x, y), permute=True) == _expected_for_swapped(eq6, (z, x, y))
x, y, z = symbols('x y z', integer=True)
eq7 = x * (2 * x + 3 * y - z)
assert diophantine(eq7, syms=(z, x, y), permute=True) == _expected_for_swapped(eq7, (z, x, y))
x, y = symbols('x y', integer=True)
eq8 = 3 * x * y + 34 * x - 12 * y + 1
assert diophantine(eq8, syms=(y, x), permute=True) == _expected_for_swapped(eq8, (y, x))
x, y = symbols('x y', integer=True)
eq9 = x ** 2 + y ** 2 + 3 * x - 5
assert diophantine(eq9, syms=(y, x), permute=True) == _expected_for_swapped(eq9, (y, x))
x, y = symbols('x y', integer=True)
eq10 = x - y
assert diophantine(eq10, syms=(y, x), permute=True) == _expected_for_swapped(eq10, (y, x))