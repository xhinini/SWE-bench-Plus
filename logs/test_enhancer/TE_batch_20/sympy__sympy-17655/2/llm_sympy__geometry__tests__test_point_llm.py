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