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