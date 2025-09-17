from sympy import S
from sympy.geometry import Point, Point2D, Point3D
from sympy.utilities.pytest import raises

def test_point_class_has_no_as_coeff_Mul():
    assert not hasattr(Point, 'as_coeff_Mul')

def test_point2d_class_has_no_as_coeff_Mul():
    assert not hasattr(Point2D, 'as_coeff_Mul')

def test_point3d_class_has_no_as_coeff_Mul():
    assert not hasattr(Point3D, 'as_coeff_Mul')

def test_point_instance_calling_as_coeff_Mul_raises_attribute_error():
    p = Point(1, 2)
    assert not hasattr(p, 'as_coeff_Mul')
    with raises(AttributeError):
        p.as_coeff_Mul()

def test_point2d_instance_calling_as_coeff_Mul_raises_attribute_error():
    p = Point2D(1, 2)
    assert not hasattr(p, 'as_coeff_Mul')
    with raises(AttributeError):
        p.as_coeff_Mul()

def test_point3d_instance_calling_as_coeff_Mul_raises_attribute_error():
    p = Point3D(1, 2, 3)
    assert not hasattr(p, 'as_coeff_Mul')
    with raises(AttributeError):
        p.as_coeff_Mul()

def test_dir_on_point_has_no_as_coeff_Mul():
    p = Point(0, 0)
    assert 'as_coeff_Mul' not in dir(p)
    assert 'as_coeff_Mul' not in dir(Point)

def test_dir_on_point2d_has_no_as_coeff_Mul():
    p = Point2D(0, 0)
    assert 'as_coeff_Mul' not in dir(p)
    assert 'as_coeff_Mul' not in dir(Point2D)

def test_dir_on_point3d_has_no_as_coeff_Mul():
    p = Point3D(0, 0, 0)
    assert 'as_coeff_Mul' not in dir(p)
    assert 'as_coeff_Mul' not in dir(Point3D)

from sympy import sin, exp
from sympy import Symbol, sqrt
from sympy.geometry import Point, Point3D
x = Symbol('x')

def test_point2d_mul_by_sin():
    p = Point(1, 2)
    assert p * sin(x) == Point(sin(x), 2 * sin(x))

def test_point2d_mul_by_exp():
    p = Point(3, 5)
    assert p * exp(x) == Point(3 * exp(x), 5 * exp(x))

def test_point2d_mul_by_pow_symbol():
    p = Point(1, 4)
    assert p * x ** 2 == Point(x ** 2, 4 * x ** 2)

def test_point2d_mul_by_compound_pow():
    p = Point(2, 3)
    assert p * (x + 1) ** 3 == Point(2 * (x + 1) ** 3, 3 * (x + 1) ** 3)

def test_point2d_mul_by_sqrt():
    p = Point(1, 2)
    assert p * sqrt(x) == Point(sqrt(x), 2 * sqrt(x))

def test_point3d_mul_by_sin():
    p = Point3D(1, 2, 3)
    assert p * sin(x) == Point3D(sin(x), 2 * sin(x), 3 * sin(x))

def test_point3d_mul_by_pow_symbol():
    p = Point3D(2, 0, 5)
    assert p * x ** 2 == Point3D(2 * x ** 2, 0, 5 * x ** 2)

def test_point3d_mul_by_sqrt():
    p = Point3D(1, 1, 1)
    assert p * sqrt(x) == Point3D(sqrt(x), sqrt(x), sqrt(x))

def test_point2d_mul_by_symbolic_pow_x_pow_x():
    p = Point(1, 2)
    assert p * x ** x == Point(x ** x, 2 * x ** x)

from sympy import sqrt, Symbol, pi, Rational
from sympy import sin
from sympy.geometry import Point, Point3D, Point2D

def test_mul_point_by_sqrt_pow():
    p = Point(1, 1)
    assert p * sqrt(2) == Point(sqrt(2), sqrt(2))
    p3 = Point3D(1, 2, 3)
    assert p3 * sqrt(2) == Point3D(sqrt(2), 2 * sqrt(2), 3 * sqrt(2))

from sympy import sqrt, Symbol, Rational
from sympy.geometry import Point, Point3D
from sympy import sqrt, Symbol, Rational
from sympy.geometry import Point, Point3D

def test_mul_by_pow_scalar_right():
    s2 = sqrt(2)
    p = Point(1, 2)
    expected = Point(s2, 2 * s2)
    assert p * s2 == expected

from sympy import Symbol, sqrt, sin, log, S
from sympy.geometry import Point, Point2D, Point3D
x = Symbol('x')

def test_point2d_mul_by_sqrt():
    p = Point2D(1, 2)
    expr = sqrt(2)
    assert p * expr == Point2D(expr, 2 * expr)

def test_point3d_mul_by_sqrt():
    p = Point3D(1, 2, 3)
    expr = sqrt(2)
    assert p * expr == Point3D(expr, 2 * expr, 3 * expr)

def test_point_mul_by_sin_symbol():
    p = Point(1, 2)
    expr = sin(x)
    assert p * expr == Point(expr, 2 * expr)

def test_point_mul_by_symbolic_pow():
    p = Point(1, 2)
    expr = x ** S.Half
    assert p * expr == Point(expr, 2 * expr)

from sympy import Symbol, sqrt, pi
from sympy.geometry import Point, Point2D, Point3D

def test_point2d_mul_by_sqrt_constant():
    p = Point(1, 2)
    assert p * sqrt(2) == Point(sqrt(2), 2 * sqrt(2))

def test_point3d_mul_by_pi():
    p3 = Point3D(1, 2, 3)
    assert p3 * pi == Point3D(pi, 2 * pi, 3 * pi)

def test_point2d_mul_by_polynomial_power():
    x = Symbol('x')
    p = Point(1, 2)
    expr = (x + 1) ** 2
    assert p * expr == Point(expr, 2 * expr)

def test_point_mul_by_sqrt_of_symbol():
    x = Symbol('x')
    p = Point(1, 1)
    assert p * sqrt(x) == Point(sqrt(x), sqrt(x))

from sympy import Symbol, Rational
from sympy.geometry import Point
from sympy.utilities.pytest import raises
from sympy import Symbol, Rational
from sympy.geometry import Point
from sympy.utilities.pytest import raises

def test_add_scaled_point_with_symbol_raises():
    x = Symbol('x')
    p = Point(1, 1)
    q = Point(2, 3)
    raises(ValueError, lambda: p + x * q)

def test_add_scaled_point_with_add_factor_raises():
    x = Symbol('x')
    p = Point(1, 1)
    q = Point(2, 3)
    raises(ValueError, lambda: p + (x + 1) * q)

def test_add_scaled_point_with_negated_symbol_raises():
    x = Symbol('x')
    p = Point(1, 1)
    q = Point(2, 3)
    raises(ValueError, lambda: p + -x * q)

def test_add_scaled_point_with_two_term_product_raises():
    x = Symbol('x')
    p = Point(1, 1)
    q = Point(2, 3)
    raises(ValueError, lambda: p + 2 * x * q)

def test_add_scaled_point_with_float_symbol_product_raises():
    x = Symbol('x')
    p = Point(1, 1)
    q = Point(2, 3)
    raises(ValueError, lambda: p + 0.5 * x * q)

from sympy import sqrt, pi, Symbol
from sympy.geometry import Point
from sympy import sqrt, pi, Symbol
from sympy.geometry import Point
from sympy import S

def test_mul_pow_right():
    p = Point(1, 2)
    assert p * sqrt(2) == Point(sqrt(2), 2 * sqrt(2))

def test_mul_pi_right():
    p = Point(1, 2)
    assert p * pi == Point(pi, 2 * pi)

from sympy import sqrt, sin, pi, S, symbols
from sympy.geometry import Point
x = symbols('x')

def test_mul_by_sqrt_right():
    p = Point(1, 2)
    assert p * sqrt(2) == Point(sqrt(2), 2 * sqrt(2))

def test_mul_by_symbolic_pow_right():
    p = Point(1, 1)
    assert p * x ** 2 == Point(x ** 2, x ** 2)

def test_mul_by_fractional_power():
    p = Point(3, 4)
    assert p * x ** S.Half == Point(3 * x ** S.Half, 4 * x ** S.Half)

def test_mul_by_function_right():
    p = Point(2, 3)
    assert p * sin(x) == Point(2 * sin(x), 3 * sin(x))

def test_mul_by_compound_pow():
    p = Point(1, 2)
    expr = (x + 1) ** 2
    assert p * expr == Point(expr, 2 * expr)

def test_mul_by_pi_sqrt():
    p = Point(1, 2)
    expr = pi ** S.Half
    assert p * expr == Point(expr, 2 * expr)