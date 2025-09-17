from sympy import sqrt, Symbol
from sympy.geometry import Point

def test_base_point_distance_truncates_extra_coordinate_simple():
    p_short = Point(0, 0, 0, 0)
    p_long = Point(0, 0, 0, 3, 4)
    assert p_short.distance(p_long) == 3

def test_base_point_distance_truncates_extra_coordinate_reverse_order():
    p_short = Point(0, 0, 0, 0)
    p_long = Point(0, 0, 0, 3, 4)
    assert p_long.distance(p_short) == 3

def test_base_point_distance_ignores_last_coordinate_when_prefix_equal():
    p1 = Point(1, 2, 3, 4)
    p2 = Point(1, 2, 3, 4, 6)
    assert p1.distance(p2) == 0

def test_base_point_distance_with_negative_values_truncates():
    p_short = Point(-1, -2, 0, 0)
    p_long = Point(-1, -2, 5, 0, 7)
    assert p_short.distance(p_long) == 5

def test_base_point_distance_multiple_extra_coords_truncated():
    p_short = Point(0, 0, 0, 1)
    p_long = Point(0, 0, 0, 4, 9, 16)
    assert p_short.distance(p_long) == 3

def test_base_point_distance_symbolic_truncation():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    p_short = Point(0, 0, 0, 0)
    p_long = Point(0, 0, 0, x, y)
    assert p_short.distance(p_long) == sqrt(x ** 2)

def test_base_point_distance_prefix_mismatch_truncates_properly():
    p_short = Point(0, 0, 2, 0)
    p_long = Point(0, 0, 5, 0, 100)
    assert p_short.distance(p_long) == 3

def test_base_point_distance_longer_prefix_zeros_truncated():
    p_short = Point(0, 0, 0, 0)
    p_long = Point(0, 7, 0, 0, 1, 2)
    assert p_short.distance(p_long) == 7

def test_base_point_distance_all_prefix_equal_extra_ignored():
    p_short = Point(3, 3, 3, 3)
    p_long = Point(3, 3, 3, 3, 999, 1000)
    assert p_short.distance(p_long) == 0

from sympy import Symbol, sqrt
from sympy.geometry import Point, Point2D, Point3D

def test_distance_generic_points_diff_dims_zero():
    p4 = Point(1, 2, 3, 4)
    p5 = Point(1, 2, 3, 4, 5)
    assert p4.distance(p5) == 0

def test_distance_generic_points_diff_dims_zero_symmetry():
    p4 = Point(2, 3, 5, 7)
    p5 = Point(2, 3, 5, 7, 11)
    assert p4.distance(p5) == 0
    assert p5.distance(p4) == 0

def test_distance_generic_points_symbolic_tail_ignored():
    x = Symbol('x', real=True)
    p4 = Point(1, 2, 3, 4)
    p5 = Point(1, 2, 3, 4, x)
    assert p4.distance(p5) == 0

def test_distance_generic_points_extra_nonzero_ignored():
    p4 = Point(0, 0, 0, 0)
    p5 = Point(0, 0, 0, 0, 5)
    assert p4.distance(p5) == 0

def test_distance_generic_points_multiple_extra_coords_ignored():
    p4 = Point(1, 2, 3, 4)
    p6 = Point(1, 2, 3, 4, 5, 6)
    assert p4.distance(p6) == 0
    assert p6.distance(p4) == 0

def test_distance_generic_points_with_negatives_ignored():
    p4 = Point(-1, -2, -3, -4)
    p5 = Point(-1, -2, -3, -4, -10)
    assert p4.distance(p5) == 0

def test_distance_generic_points_longer_diff_nonzero_various():
    p4 = Point(9, 8, 7, 6)
    p5 = Point(9, 8, 7, 6, 1)
    assert p4.distance(p5) == 0

from __future__ import division
from sympy import Point, Symbol, sqrt

def test_distance_generic_point_diff_len_trailing_nonzero_ignored():
    p4 = Point(1, 2, 3, 4)
    p5 = Point(1, 2, 3, 4, 5)
    assert p4.distance(p5) == 0

def test_distance_generic_point_diff_len_trailing_nonzero_ignored_reverse():
    p4 = Point(1, 2, 3, 4)
    p5 = Point(1, 2, 3, 4, 5)
    assert p5.distance(p4) == 0

def test_distance_generic_point_early_coord_difference_respected_extra_ignored():
    p4 = Point(1, 2, 3, 4)
    p5 = Point(2, 2, 3, 4, 5)
    assert p4.distance(p5) == 1

def test_distance_generic_point_second_coord_difference_extra_ignored():
    p4 = Point(1, 2, 3, 4)
    p5 = Point(1, 3, 3, 4, 7)
    assert p4.distance(p5) == 1

def test_distance_generic_point_negative_coords_extra_ignored():
    p4 = Point(-1, -2, -3, -4)
    p5 = Point(-1, -2, -3, -4, 10)
    assert p4.distance(p5) == 0

def test_distance_longer_point_against_shorter_same_prefix_ignored_tail():
    p6 = Point(1, 2, 3, 4, 5, 6)
    p4 = Point(1, 2, 3, 4)
    assert p6.distance(p4) == 0

def test_distance_longer_point_with_early_difference_extra_ignored():
    p6 = Point(1, 2, 3, 4, 5, 6)
    p4 = Point(1, 99, 3, 4)
    assert p6.distance(p4) == 97

def test_distance_generic_point_symbolic_extra_ignored():
    a = Symbol('a')
    p4 = Point(0, 0, 0, 0)
    p5 = Point(0, 0, 0, 0, a)
    assert p4.distance(p5) == 0

def test_distance_generic_point_float_coords_extra_ignored():
    p4 = Point(1.0, 2.0, 3.0, 4.0)
    p5 = Point(1.0, 2.0, 3.0, 4.0, 2.5)
    assert p4.distance(p5) == 0