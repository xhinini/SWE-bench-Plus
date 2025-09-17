from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.combinatorics.named_groups import DihedralGroup
from sympy.testing.pytest import raises

def test_regression_perm_single_generator_invalid():
    a = Permutation(0, 1, 2)
    b = Permutation(0, 1)
    G = PermutationGroup([a, b])
    raises(ValueError, lambda: homomorphism(G, G, [a], [a]))

def test_regression_dihedral_swap_generators_invalid():
    D = DihedralGroup(8)
    gens = list(D.generators)
    raises(ValueError, lambda: homomorphism(D, D, gens, [gens[1], gens[0]]))

def test_regression_perm_three_generators_invalid():
    a = Permutation(0, 1, 2, 3)
    b = Permutation(0, 2)(1, 3)
    c = Permutation(0, 3)(1, 2)
    G = PermutationGroup([a, b, c])
    raises(ValueError, lambda: homomorphism(G, G, [a, b, c], [a, a, c]))