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

from sympy.geometry import Point, Point2D, Point3D
from sympy.core.numbers import I
from sympy.testing.pytest import raises

def test_point_rejects_imaginary_coordinate_with_evaluate_false():
    with raises(ValueError):
        Point(0, I, evaluate=False)

def test_point_rejects_imaginary_coordinate_list_input_evaluate_false():
    with raises(ValueError):
        Point([1, I], evaluate=False)

def test_point_rejects_imaginary_coordinate_tuple_input_evaluate_false():
    with raises(ValueError):
        Point((1, I), evaluate=False)

def test_point_rejects_complex_number_with_evaluate_false():
    with raises(ValueError):
        Point(3 + I, 0, evaluate=False)

def test_point2d_rejects_imaginary_coordinate_with_evaluate_false():
    with raises(ValueError):
        Point2D(1, I, evaluate=False)

def test_point2d_rejects_complex_coordinate_with_evaluate_false():
    with raises(ValueError):
        Point2D(1 + I, 0, evaluate=False)

def test_point3d_rejects_imaginary_coordinate_with_evaluate_false():
    with raises(ValueError):
        Point3D(I, 0, 0, evaluate=False)

def test_point3d_rejects_complex_coordinate_with_evaluate_false():
    with raises(ValueError):
        Point3D(0, 1 + 2 * I, 2, evaluate=False)

def test_mixed_list_and_tuple_imaginary_rejection_evaluate_false():
    with raises(ValueError):
        Point([0, 0, I], evaluate=False)
    with raises(ValueError):
        Point((I, 0, 0), evaluate=False)

from sympy import I
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises

def test_point_imaginary_evaluate_false_simple():
    with raises(ValueError):
        Point(3, I, evaluate=False)

def test_point_imaginary_evaluate_false_mixed():
    with raises(ValueError):
        Point(3 + I, 2, evaluate=False)

def test_point_imaginary_evaluate_false_tuple_input():
    with raises(ValueError):
        Point((1, I), evaluate=False)

def test_point_imaginary_evaluate_false_list_input():
    with raises(ValueError):
        Point([1, I], evaluate=False)

def test_point2d_imaginary_evaluate_false():
    with raises(ValueError):
        Point2D(1, I, evaluate=False)

def test_point3d_imaginary_evaluate_false():
    with raises(ValueError):
        Point3D(1, 2, I, evaluate=False)

def test_point_imaginary_with_float_and_evaluate_false():
    with raises(ValueError):
        Point(1.0, I, evaluate=False)

def test_point_imaginary_with_zero_and_evaluate_false():
    with raises(ValueError):
        Point(0, I, evaluate=False)

def test_point_imaginary_multiple_coords_evaluate_false():
    with raises(ValueError):
        Point(1, 2, 3, I, evaluate=False)

from sympy import I
from sympy import I
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises

def test_point_rejects_imaginary_with_evaluate_false():
    raises(ValueError, lambda: Point(1 + I, 2, evaluate=False))

def test_point2d_rejects_imaginary_with_evaluate_false():
    raises(ValueError, lambda: Point2D(1 + I, 2, evaluate=False))

def test_point3d_rejects_imaginary_with_evaluate_false():
    raises(ValueError, lambda: Point3D(1 + I, 2, 3, evaluate=False))

def test_point_with_tuple_and_evaluate_false_rejects_imaginary():
    raises(ValueError, lambda: Point((1 + I, 2), evaluate=False))

def test_point_with_list_and_evaluate_false_rejects_imaginary():
    raises(ValueError, lambda: Point([1 + I, 2], evaluate=False))

def test_point_float_plus_imag_rejects_with_evaluate_false():
    raises(ValueError, lambda: Point(1.0 + I, 2, evaluate=False))

def test_point_on_morph_ignore_and_evaluate_false_rejects_imaginary():
    raises(ValueError, lambda: Point(1 + I, 2, dim=3, on_morph='ignore', evaluate=False))

def test_point2d_construct_from_list_rejects_imaginary_evaluate_false():
    raises(ValueError, lambda: Point2D([1 + I, 2], evaluate=False))

from sympy.core.numbers import I
from sympy.core.symbol import Symbol
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises

def test_imaginary_coordinates_rejected_evaluate_false_args():
    raises(ValueError, lambda: Point(1 + I, 0, evaluate=False))

def test_imaginary_coordinates_rejected_evaluate_false_sequence():
    raises(ValueError, lambda: Point((1 + I, 0), evaluate=False))

def test_point2d_imaginary_rejected_evaluate_false():
    raises(ValueError, lambda: Point2D(1 + I, 0, evaluate=False))

def test_point3d_imaginary_rejected_evaluate_false():
    raises(ValueError, lambda: Point3D(1, 0, 2 * I, evaluate=False))

def test_padding_dims_imaginary_rejected():
    raises(ValueError, lambda: Point((1 + I, 0), dim=3, evaluate=False))

def test_imaginary_in_point2d_sequence_rejected():
    raises(ValueError, lambda: Point2D((1 + I, 0), evaluate=False))

from sympy.geometry import Point, Point2D, Point3D
from sympy.core.numbers import I
from sympy.testing.pytest import raises
from sympy.geometry import Point, Point2D, Point3D
from sympy.core.numbers import I

def test_point_imaginary_coordinate_raises_evaluate_false():
    with raises(ValueError):
        Point(1, I, evaluate=False)

def test_point_imaginary_coordinate_sum_raises_evaluate_false():
    with raises(ValueError):
        Point(1 + I, 2, evaluate=False)

def test_point_tuple_with_imaginary_raises_evaluate_false():
    with raises(ValueError):
        Point((1, I), evaluate=False)

def test_point_list_with_imaginary_raises_evaluate_false():
    with raises(ValueError):
        Point([1, I], evaluate=False)

def test_point2d_imaginary_coordinate_raises_evaluate_false():
    with raises(ValueError):
        Point2D(1, I, evaluate=False)

def test_point3d_imaginary_coordinate_raises_evaluate_false():
    with raises(ValueError):
        Point3D(1, I, 0, evaluate=False)

def test_point_imaginary_as_first_coordinate_raises_evaluate_false():
    with raises(ValueError):
        Point(I, 0, evaluate=False)

def test_point_higher_dimension_imaginary_raises_evaluate_false():
    with raises(ValueError):
        Point(1, 0, I, 0, evaluate=False)

def test_point_with_dim_padding_and_imaginary_raises_evaluate_false():
    with raises(ValueError):
        Point(1, I, dim=3, on_morph='ignore', evaluate=False)

# No extra imports required beyond those in the test file.
from sympy import I, S
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises


def test_imag_coordinate_rejected_point_evaluate_false_2d():
    # Even with evaluate=False, imaginary coordinates must be rejected
    raises(ValueError, lambda: Point(1, I, evaluate=False))

def test_imag_coordinate_rejected_point_evaluate_false_3d():
    raises(ValueError, lambda: Point(1, 2, I, evaluate=False))

def test_imag_coordinate_rejected_point2d_evaluate_false():
    raises(ValueError, lambda: Point2D(1, I, evaluate=False))

def test_imag_coordinate_rejected_point3d_evaluate_false():
    raises(ValueError, lambda: Point3D(1, I, 3, evaluate=False))

def test_imag_coordinate_rejected_from_tuple_evaluate_false():
    # passing a tuple with an imaginary component should fail even if evaluate=False
    raises(ValueError, lambda: Point((1, I), evaluate=False))

def test_imag_coordinate_rejected_symbolic_imag_evaluate_false():
    # symbolic expression with imaginary part should be rejected regardless of evaluate flag
    raises(ValueError, lambda: Point(1 + I, 2, evaluate=False))

def test_imag_coordinate_rejected_with_dim_padding_evaluate_false():
    # when dim forces padding, the imaginary check should still be applied
    raises(ValueError, lambda: Point((1, I), dim=3, on_morph='ignore', evaluate=False))

def test_imag_coordinate_rejected_mixed_types_evaluate_false():
    # mixed ordering: imaginary in first position
    raises(ValueError, lambda: Point(I, S.Zero, evaluate=False))

def test_imag_coordinate_rejected_nested_sequence_evaluate_false():
    # nested sequence that flattens to an imaginary coordinate is invalid
    raises(ValueError, lambda: Point([1, I], evaluate=False))

def test_imag_coordinate_rejected_when_constructing_from_point_with_imag_component():
    # constructing from an existing sequence that contains imaginary coordinate
    # should raise even when evaluate=False
    raises(ValueError, lambda: Point((S.One + I, S.One), evaluate=False))

from sympy import I, sympify
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises
from sympy import I, sympify
from sympy.geometry import Point, Point2D, Point3D
from sympy.testing.pytest import raises

def test_point_imaginary_raises_explicit_evaluate_false():
    raises(ValueError, lambda: Point(1 + I, 2, evaluate=False))

def test_point_second_coordinate_imaginary_evaluate_false():
    raises(ValueError, lambda: Point(0, I, evaluate=False))

def test_point_from_tuple_imaginary_evaluate_false():
    raises(ValueError, lambda: Point((1 + I, 0), evaluate=False))

def test_point_from_list_imaginary_evaluate_false():
    raises(ValueError, lambda: Point([0, 2 * I], evaluate=False))

def test_point_with_sympified_imaginary_evaluate_false():
    raises(ValueError, lambda: Point(sympify('I'), 1, evaluate=False))

def test_point_with_float_and_imaginary_evaluate_false():
    raises(ValueError, lambda: Point(0.5, I, evaluate=False))

def test_point2d_imaginary_in_constructor_evaluate_false():
    raises(ValueError, lambda: Point2D(1 + I, 2, evaluate=False))