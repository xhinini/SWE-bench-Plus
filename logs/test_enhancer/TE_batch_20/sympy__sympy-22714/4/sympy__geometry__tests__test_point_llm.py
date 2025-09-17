from sympy import Point, Point2D, Point3D, I
from sympy.testing.pytest import raises

def test_point_imaginary_coordinate_evaluate_false_simple():
    raises(ValueError, lambda: Point(1, I, evaluate=False))

def test_point_imaginary_coordinate_evaluate_false_with_real_part():
    raises(ValueError, lambda: Point(1 + I, 2, evaluate=False))

def test_point2d_imaginary_coordinate_evaluate_false():
    raises(ValueError, lambda: Point2D(1, I, evaluate=False))

def test_point3d_imaginary_coordinate_evaluate_false():
    raises(ValueError, lambda: Point3D(1, 2, I, evaluate=False))

def test_higher_dim_point_imaginary_coordinate_evaluate_false():
    raises(ValueError, lambda: Point(1, 2, 3, I, dim=4, evaluate=False))

def test_point_imaginary_with_padding_dim_evaluate_false():
    raises(ValueError, lambda: Point(1, I, dim=3, evaluate=False))

def test_point_construct_from_sequence_imaginary_evaluate_false():
    raises(ValueError, lambda: Point([1, I], evaluate=False))

def test_add_sequence_with_imaginary_raises():
    raises(ValueError, lambda: Point(1, 2) + (I, 0))

def test_subtract_sequence_with_imaginary_raises():
    raises(ValueError, lambda: Point(1, 2) - (I, 0))

from sympy import Point, Point2D, Point3D, I
from sympy.testing.pytest import raises

def test_point_imaginary_evaluate_false():
    raises(ValueError, lambda: Point(1, I, evaluate=False))

def test_point_imaginary_sequence_evaluate_false():
    raises(ValueError, lambda: Point([1, I], evaluate=False))

def test_point2d_imaginary_evaluate_false():
    raises(ValueError, lambda: Point2D(1, I, evaluate=False))

def test_point3d_imaginary_evaluate_false():
    raises(ValueError, lambda: Point3D(1, 2, I, evaluate=False))

def test_point_imaginary_with_float_evaluate_false():
    raises(ValueError, lambda: Point(1.0, I, evaluate=False))

def test_add_with_imaginary_in_tuple_raises():
    raises(ValueError, lambda: Point(1, 2) + (3, I))