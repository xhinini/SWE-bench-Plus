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