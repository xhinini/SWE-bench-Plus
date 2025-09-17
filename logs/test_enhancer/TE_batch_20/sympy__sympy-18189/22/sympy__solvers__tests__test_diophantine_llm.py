# No new imports required beyond those used in the test body.
from sympy import symbols, Eq, S
from sympy.abc import x, y, z
from sympy.utilities.iterables import signed_permutations
from sympy.solvers.diophantine import diophantine, diop_solve

# 1) Even powers sum (canonical example from docs)
a, b = symbols('a b', integer=True)
eq = a**4 + b**4 - (2**4 + 3**4)
# base solution (no permute)
assert diophantine(eq) == {(2, 3)}
# permuted solutions must match signed permutations of base (order matters)
expected = set(signed_permutations((2, 3)))
assert diophantine(eq, permute=True) == expected
# reversed syms ordering should produce same set but with swapped tuple positions
res_xy = diophantine(eq, syms=(a, b), permute=True)
res_yx = diophantine(eq, syms=(b, a), permute=True)
# convert res_yx into a,b order by swapping entries in each tuple
swapped = { (t[1], t[0]) for t in res_yx }
assert swapped == res_xy == expected

# 2) Linear equation: ensure syms ordering and permute handling is consistent
u, v = symbols('u v', integer=True)
eq_lin = u - 3*v + 2
# The solver returns paramized tuple in order of free symbols; test with swap
sol_uv = diophantine(eq_lin, syms=(u, v))
sol_vu = diophantine(eq_lin, syms=(v, u))
# convert sol_vu back to u,v order
converted = { (s[1], s[0]) for s in sol_vu }
assert sol_uv == converted

# 3) Linear with permute flag (should not change linear param output,
# but ensure passing permute does not break syms handling)
assert diophantine(eq_lin, syms=(u, v), permute=True) == sol_uv
assert diophantine(eq_lin, syms=(v, u), permute=True) == sol_vu

# 4) Ternary quadratic: reorder syms and ensure mapping is correct
p, q, r = symbols('p q r', integer=True)
eq_tern = x**2 + y**2 - z**2
base = diophantine(eq_tern)  # base solution uses (x,y,z) order
# Permuted variable order should reflect corresponding tuple reordering
s_xyz = diophantine(eq_tern, syms=(x, y, z))
s_zxy = diophantine(eq_tern, syms=(z, x, y))
# convert z,x,y order back to x,y,z
conv = { (t[1], t[2], t[0]) for t in s_zxy }
assert conv == s_xyz == base

# 5) general_sum_of_squares: ensure syms ordering doesn't change the set
a1, a2, a3 = symbols('a1 a2 a3', integer=True)
eq_gs = a1**2 + a2**2 + a3**2 - (1 + 4 + 9)
base_gs = diophantine(eq_gs)
# swap first two symbols in ordering
swapped_gs = diophantine(eq_gs, syms=(a2, a1, a3))
# convert swapped_gs tuples back to original order
conv_gs = { (t[1], t[0], t[2]) for t in swapped_gs }
assert conv_gs == base_gs

# 6) Ensure partial reordering with same symbol set but different order
# This checks that providing a permutation of all variables is handled.
eq2 = y**4 + x**4 - 2**4 - 3**4
sol_xy = diophantine(eq2, syms=(x, y), permute=True)
sol_yx = diophantine(eq2, syms=(y, x), permute=True)
# converting yx -> xy order should match
conv2 = { (t[1], t[0]) for t in sol_yx }
assert conv2 == sol_xy

# 7) Ensure diop_solve/univariate interplay with syms where applicable
# (calls diop_solve through diophantine pipeline for simple factorable cases)
# Example: (x - y)*(x**2 + y**2 - z**2) with syms swapped
eq_mix = (x - y)*(x**2 + y**2 - z**2)
sol_default = diophantine(eq_mix)
sol_swapped = diophantine(eq_mix, syms=(y, x, z))
# swap back y,x,z -> x,y,z
conv_mix = { (t[1], t[0], t[2]) for t in sol_swapped }
assert conv_mix == sol_default

# 8) Confirm no exceptions are raised when syms is a tuple (sequence) and permute=True
# for a simple case that uses sign permutations.
assert isinstance(diophantine(eq, syms=(a, b), permute=True), set)

# 9) Consistency: calling diophantine with the natural variable order vs explicit syms
eq_cons = x**2 - x - y**2
natural = diophantine(eq_cons)
explicit = diophantine(eq_cons, syms=(x, y))
assert natural == explicit

# 10) Ensure that providing syms as a list in a different order yields results that can be
# mapped back to the canonical var order deterministically (no exceptions)
s1 = diophantine(eq_cons, syms=[y, x])
# convert y,x back to x,y
s1_conv = { (t[1], t[0]) for t in s1 }
assert s1_conv == natural
