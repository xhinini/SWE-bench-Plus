from sympy.polys.rings import ring
from sympy.polys.domains import ZZ
from sympy.testing.pytest import raises
from sympy.core import symbols as sympy_symbols, Symbol

def test_as_expr_rejects_polyelement_tuple():
    R, x, y, z = ring('x,y,z', ZZ)
    f = 3 * x ** 2 * y - x * y * z + 7 * z ** 3 + 1
    raises(Exception, lambda: f.as_expr(x, y, z))

def test_as_expr_rejects_polyelement_list_splat():
    R, x, y, z = ring('x,y,z', ZZ)
    f = x + y + z
    raises(Exception, lambda: f.as_expr(*[x, y, z]))

def test_as_expr_rejects_mixed_poly_and_sympy_symbol():
    R, x, y, z = ring('x,y,z', ZZ)
    U, V, W = sympy_symbols('u,v,w')
    f = 3 * x ** 2 * y - x * y * z + 7 * z ** 3 + 1
    raises(Exception, lambda: f.as_expr(x, y, W))

def test_as_expr_rejects_generators_from_different_ring():
    R1, x1, y1, z1 = ring('x,y,z', ZZ)
    R2, a, b, c = ring('a,b,c', ZZ)
    f = 5 * x1 * y1 + z1
    raises(Exception, lambda: f.as_expr(a, b, c))

def test_as_expr_rejects_reordered_poly_generators():
    R, x, y, z = ring('x,y,z', ZZ)
    f = x * y + z
    raises(Exception, lambda: f.as_expr(z, y, x))

def test_as_expr_rejects_repeated_poly_generators():
    R, x, y, z = ring('x,y,z', ZZ)
    f = x + y + z
    raises(Exception, lambda: f.as_expr(x, x, x))

def test_as_expr_rejects_mixed_list_containing_polyelements():
    R, x, y, z = ring('x,y,z', ZZ)
    lst = [x, y, Symbol('u')]
    f = x * y + z
    raises(Exception, lambda: f.as_expr(*lst))

def test_as_expr_univariate_rejects_polyelement_symbol():
    R, t = ring('t', ZZ)
    f = t ** 2 + 1
    raises(Exception, lambda: f.as_expr(t))

def test_as_expr_rejects_mix_of_rings_and_symbols():
    R1, x1, y1, z1 = ring('x,y,z', ZZ)
    R2, a, b, c = ring('a,b,c', ZZ)
    f = x1 ** 2 + y1
    raises(Exception, lambda: f.as_expr(x1, a, Symbol('u')))