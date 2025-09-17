from sympy.testing.pytest import raises
from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray
from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray, MutableSparseNDimArray
from sympy.testing.pytest import raises
from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray
from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray, MutableSparseNDimArray

def test_parse_index_integer_in_bounds_immutable_dense_1d():
    a = ImmutableDenseNDimArray([1, 2, 3])
    assert a._parse_index(1) == 1

def test_parse_index_integer_in_bounds_mutable_dense_1d():
    a = MutableDenseNDimArray([1, 2, 3])
    assert a._parse_index(2) == 2

def test_parse_index_integer_in_bounds_immutable_dense_2d():
    a = ImmutableDenseNDimArray([[1, 2, 3], [4, 5, 6]])
    assert a._parse_index(4) == 4

def test_parse_index_integer_in_bounds_mutable_sparse_1d():
    a = MutableSparseNDimArray([10, 20, 30])
    assert a._parse_index(0) == 0

def test_parse_index_negative_integer_dense_returns_negative():
    a = ImmutableDenseNDimArray([1, 2, 3])
    assert a._parse_index(-1) == -1

from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray
from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray, MutableSparseNDimArray

def test_scan_iterable_shape_empty_ambiguous_immutable_dense():
    amb = AmbiguousBoolList()
    res = ImmutableDenseNDimArray._scan_iterable_shape(amb)
    assert res == ([], (0,))

def test_scan_iterable_shape_empty_ambiguous_mutable_dense():
    amb = AmbiguousBoolList()
    res = MutableDenseNDimArray._scan_iterable_shape(amb)
    assert res == ([], (0,))

def test_scan_iterable_shape_list_with_empty_ambiguous_immutable_dense():
    amb = AmbiguousBoolList()
    res = ImmutableDenseNDimArray._scan_iterable_shape([amb])
    assert res == ([], (1, 0))

def test_scan_iterable_shape_nested_empty_ambiguous_mutable_dense():
    amb = AmbiguousBoolList()
    res = MutableDenseNDimArray._scan_iterable_shape([[amb]])
    assert res == ([], (1, 1, 0))

def test_scan_iterable_shape_ambiguous_nonempty_top_level_immutable_dense():
    amb = AmbiguousBoolList([1, 2])
    res = ImmutableDenseNDimArray._scan_iterable_shape(amb)
    assert res == ([1, 2], (2,))

def test_scan_iterable_shape_list_with_ambiguous_nonempty_mutable_dense():
    amb = AmbiguousBoolList([1, 2])
    res = MutableDenseNDimArray._scan_iterable_shape([amb])
    assert res == ([1, 2], (1, 2))

def test_scan_iterable_shape_double_nested_ambiguous_nonempty_immutable_sparse():
    amb = AmbiguousBoolList([1, 2])
    res = ImmutableSparseNDimArray._scan_iterable_shape([[amb]])
    assert res == ([1, 2], (1, 1, 2))

def test_scan_iterable_shape_ambiguous_nonempty_mutable_sparse_top_level():
    amb = AmbiguousBoolList([1, 2])
    res = MutableSparseNDimArray._scan_iterable_shape(amb)
    assert res == ([1, 2], (2,))

def test_scan_iterable_shape_inner_two_empties_immutable_dense():
    amb1 = AmbiguousBoolList()
    amb2 = AmbiguousBoolList()
    res = ImmutableDenseNDimArray._scan_iterable_shape([[amb1, amb2]])
    assert res == ([], (1, 2, 0))

from sympy.testing.pytest import raises
from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray
from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray, MutableSparseNDimArray

def test_mutable_assignment_with_integer_index():
    A = MutableDenseNDimArray([0, 1, 2])
    A[1] = 99
    assert A[1] == 99
    assert A[0] == 0 and A[2] == 2

from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray

def test_ambiguous_iterable_empty_immutable():
    A = ImmutableDenseNDimArray(AmbiguousIterable([]))
    assert isinstance(A, ImmutableDenseNDimArray)
    assert A.shape == (0,)
    assert list(A) == []

def test_ambiguous_iterable_empty_mutable():
    A = MutableDenseNDimArray(AmbiguousIterable([]))
    assert isinstance(A, MutableDenseNDimArray)
    assert A.shape == (0,)
    assert list(A) == []

def test_ambiguous_iterable_nested_list_immutable():
    A = ImmutableDenseNDimArray([AmbiguousIterable([])])
    assert A.shape == (1, 0)
    assert A.tolist() == [[]]

def test_ambiguous_iterable_nested_list_mutable():
    A = MutableDenseNDimArray([AmbiguousIterable([])])
    assert A.shape == (1, 0)
    assert A.tolist() == [[]]

def test_ambiguous_iterable_double_nested_immutable():
    A = ImmutableDenseNDimArray([[AmbiguousIterable([])]])
    assert A.shape == (1, 1, 0)
    assert A.tolist() == [[[]]]

def test_ambiguous_iterable_double_nested_mutable():
    A = MutableDenseNDimArray([[AmbiguousIterable([])]])
    assert A.shape == (1, 1, 0)
    assert A.tolist() == [[[]]]

def test_ambiguous_iterable_wrapped_in_tuple_immutable():
    A = ImmutableDenseNDimArray((AmbiguousIterable([]),))
    assert A.shape == (1, 0)
    assert A.tolist() == [[]]

def test_ambiguous_iterable_wrapped_in_tuple_mutable():
    A = MutableDenseNDimArray((AmbiguousIterable([]),))
    assert A.shape == (1, 0)
    assert A.tolist() == [[]]

def test_ambiguous_iterable_tolist_nested_immutable():
    A = ImmutableDenseNDimArray([[(AmbiguousIterable([]),)]])
    assert A.shape == (1, 1, 1, 0)
    assert A.tolist() == [[[[]]]]

from sympy.testing.pytest import raises
from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray, MutableDenseNDimArray
from sympy.tensor.array.sparse_ndim_array import ImmutableSparseNDimArray, MutableSparseNDimArray

def test_indexing_empty_immutable_dense_raises_with_correct_message():
    a = ImmutableDenseNDimArray([])
    try:
        _ = a[0]
    except ValueError as e:
        assert str(e) == 'Index not valid with an empty array'
    else:
        raise AssertionError('Indexing an empty array should have raised ValueError')

def test_indexing_empty_mutable_dense_raises_with_correct_message():
    a = MutableDenseNDimArray([])
    try:
        _ = a[0]
    except ValueError as e:
        assert str(e) == 'Index not valid with an empty array'
    else:
        raise AssertionError('Indexing an empty array should have raised ValueError')