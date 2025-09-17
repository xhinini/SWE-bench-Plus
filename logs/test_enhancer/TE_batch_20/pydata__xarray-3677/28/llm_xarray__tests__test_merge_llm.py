import sys
import types
import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical

def test_merge_dataset_with_unnamed_dataarray_raises_meaningful_error():
    ds = xr.Dataset({'a': ('x', [0, 1])}, coords={'x': [0, 1]})
    da = xr.DataArray([10, 11], dims=('x',))

    def _run():
        with pytest.raises(ValueError):
            ds.merge(da)
    _with_stub_core_dataarray(_run)

import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical
from xarray import MergeError

def test_merge_with_user_defined_DataArray_wrapper(monkeypatch):
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    wrapper = DataArrayWrapper(da)
    monkeypatch.setattr(xr, 'DataArray', DataArrayWrapper)
    result = ds.merge(wrapper)
    expected = xr.merge([ds, da])
    assert_identical(result, expected)

def test_merge_with_user_defined_DataArray_wrapper_unnamed_raises(monkeypatch):
    ds = xr.Dataset({})
    da = xr.DataArray([1, 2], dims='x')
    wrapper = DataArrayWrapper(da)
    monkeypatch.setattr(xr, 'DataArray', DataArrayWrapper)
    with pytest.raises(ValueError):
        ds.merge(wrapper)

def test_merge_wrapper_override_compat(monkeypatch):
    ds = xr.Dataset({'x': 0})
    da = xr.DataArray(1, name='x')
    wrapper = DataArrayWrapper(da)
    monkeypatch.setattr(xr, 'DataArray', DataArrayWrapper)
    result = ds.merge(wrapper, compat='override')
    expected = xr.merge([ds, da], compat='override')
    assert_identical(result, expected)

def test_merge_wrapper_preserve_attrs(monkeypatch):
    data = xr.Dataset({'x': ([], 0, {'foo': 'bar'})})
    da = xr.DataArray(0, name='x')
    wrapper = DataArrayWrapper(da)
    monkeypatch.setattr(xr, 'DataArray', DataArrayWrapper)
    result = data.merge(wrapper)
    expected = xr.merge([data, da])
    assert_identical(result, expected)

import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical

def test_merge_method_converts_wrapped_dataarray_named():
    orig = _install_fake_dataarray()
    try:
        ds = xr.Dataset({'a': 0})
        fake = xr.DataArray(1, name='b')
        expected = xr.merge([ds, orig(data=1, name='b')])
        result = ds.merge(fake)
        assert_identical(result, expected)
    finally:
        _restore_dataarray(orig)

def test_merge_method_unnamed_wrapped_dataarray_raises():
    orig = _install_fake_dataarray()
    try:
        ds = xr.Dataset({'a': 0})
        fake = xr.DataArray([1, 2], dims='x')
        with pytest.raises(ValueError) as exc:
            ds.merge(fake)
        assert 'without providing an explicit name' in str(exc.value)
    finally:
        _restore_dataarray(orig)

def test_merge_method_conflict_with_wrapped_dataarray_raises_MergeError():
    orig = _install_fake_dataarray()
    try:
        ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        fake = xr.DataArray([9, 9], dims='x', coords={'x': [0, 1]}, name='a')
        with pytest.raises(xr.MergeError):
            ds.merge(fake)
    finally:
        _restore_dataarray(orig)

def test_merge_method_no_conflicts_with_wrapped_dataarray_compat_no_conflicts():
    orig = _install_fake_dataarray()
    try:
        ds1 = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        fake = xr.DataArray([2, 3], dims='x', coords={'x': [1, 2]}, name='a')
        expected = xr.merge([ds1, orig(data=[2, 3], dims=('x',), coords={'x': [1, 2]}, name='a')], compat='no_conflicts')
        result = ds1.merge(fake, compat='no_conflicts')
        assert_identical(result, expected)
    finally:
        _restore_dataarray(orig)

def test_merge_method_fill_value_with_wrapped_dataarray():
    orig = _install_fake_dataarray()
    try:
        ds1 = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        fake = xr.DataArray([3, 4], dims='x', coords={'x': [1, 2]}, name='b')
        merged = ds1.merge(fake, fill_value=0)
        assert merged['a'].values.shape[0] == 3
        assert merged['a'].values[2] == 0
    finally:
        _restore_dataarray(orig)

def test_merge_method_attaches_coords_from_wrapped_dataarray_indexer():
    orig = _install_fake_dataarray()
    try:
        ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        fake = xr.DataArray([5, 6], dims='x', coords={'x': [0, 1], 'y': ('x', [10, 11])}, name='b')
        merged = ds.merge(fake)
        assert 'y' in merged.coords
        assert np.array_equal(merged['y'].values, np.array([10, 11, np.nan])) or np.array_equal(merged['y'].values[:2], np.array([10, 11]))
    finally:
        _restore_dataarray(orig)

def test_merge_method_multiple_calls_with_wrapped_dataarray_stability():
    orig = _install_fake_dataarray()
    try:
        ds = xr.Dataset({'a': 0})
        fake = xr.DataArray(1, name='b')
        r1 = ds.merge(fake)
        r2 = ds.merge(fake)
        assert_identical(r1, r2)
    finally:
        _restore_dataarray(orig)

import pytest
import xarray as xr
import numpy as np
from xarray.testing import assert_identical

def test_merge_dataset_with_monkeypatched_dataarray_named(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake = FakeDataArray(1, name='b')
    expected = xr.Dataset({'a': 0, 'b': 1})
    result = ds.merge(fake)
    assert_identical(result, expected)

def test_merge_dataset_with_monkeypatched_dataarray_unnamed_raises(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake = FakeDataArray(1, name=None)
    with pytest.raises(ValueError):
        ds.merge(fake)

def test_merge_dataset_conflicting_var_raises_mergeerror(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake = FakeDataArray(1, name='a')
    with pytest.raises(xr.MergeError):
        ds.merge(fake)

def test_merge_dataset_with_dim_coord_alignment(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
    fake = FakeDataArray([3, 4], name='b', dims=('x',))
    result = ds.merge(fake)
    expected = xr.Dataset({'a': ('x', [1, 2]), 'b': ('x', [3, 4]), 'x': [0, 1]})
    assert_identical(result, expected)

def test_merge_dataset_multiple_sequential(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake1 = FakeDataArray(1, name='b')
    fake2 = FakeDataArray(2, name='c')
    result = ds.merge(fake1).merge(fake2)
    expected = xr.Dataset({'a': 0, 'b': 1, 'c': 2})
    assert_identical(result, expected)

def test_merge_dataset_with_unnamed_then_named(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake_named = FakeDataArray(5, name='b')
    fake_unnamed = FakeDataArray(6, name=None)
    res1 = ds.merge(fake_named)
    expected1 = xr.Dataset({'a': 0, 'b': 5})
    assert_identical(res1, expected1)
    with pytest.raises(ValueError):
        res1.merge(fake_unnamed)

def test_merge_dataset_equivalence_to_explicit_to_dataset(monkeypatch):
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray)
    ds = xr.Dataset({'a': 0})
    fake = FakeDataArray(7, name='b')
    result_via_merge = ds.merge(fake)
    result_explicit = ds.merge(fake.to_dataset())
    assert_identical(result_via_merge, result_explicit)

import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical
from xarray.core import dtypes

def test_merge_custom_dataarray_like_simple(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        fake = make_fake_da('b', 1)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        ds = xr.Dataset({'a': 0})
        result = ds.merge(fake)
        expected = xr.merge([ds, xr.Dataset({'b': 1})])
        assert_identical(result, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_with_dims(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds_return = xr.Dataset({'b': ('x', [10, 20]), 'x': [0, 1]})
        fake = make_fake_da('b', None, ds_return=ds_return)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        res = ds.merge(fake)
        expected = xr.merge([ds, ds_return])
        assert_identical(res, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_unnamed_raises(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        fake = make_fake_da(None, 2)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        ds = xr.Dataset({'a': 0})
        with pytest.raises(ValueError, match='explicit name'):
            ds.merge(fake)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_conflict_raises_mergeerror(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds = xr.Dataset({'a': 0})
        ds_conflict = xr.Dataset({'a': 1})
        fake = make_fake_da('a', None, ds_return=ds_conflict)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        with pytest.raises(xr.MergeError):
            ds.merge(fake)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_no_conflicts_compat(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds1 = xr.Dataset({'a': ('x', [1, np.nan]), 'x': [0, 1]})
        ds2 = xr.Dataset({'a': ('x', [np.nan, 2]), 'x': [0, 1]})
        fake = make_fake_da('a', None, ds_return=ds2)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        res = ds1.merge(fake, compat='no_conflicts')
        expected = xr.merge([ds1, ds2], compat='no_conflicts')
        assert_identical(res, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_with_coords(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds_return = xr.Dataset({'b': ('x', [5, 6]), 'x': [10, 11], 'coord': ('x', [0, 1])})
        fake = make_fake_da('b', None, ds_return=ds_return)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [10, 11]})
        res = ds.merge(fake)
        expected = xr.merge([ds, ds_return])
        assert_identical(res, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_fill_value(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds1 = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
        ds2 = xr.Dataset({'b': ('x', [3, 4]), 'x': [1, 2]})
        fake = make_fake_da('b', None, ds_return=ds2)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        fill_value = dtypes.NA
        res = ds1.merge(fake, fill_value=fill_value)
        expected = xr.merge([ds1, ds2], fill_value=fill_value)
        assert_identical(res, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_inner_join(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds1 = xr.Dataset({'a': ('x', [1, 2, 3]), 'x': [0, 1, 2]})
        ds2 = xr.Dataset({'b': ('x', [9, 8]), 'x': [1, 2]})
        fake = make_fake_da('b', None, ds_return=ds2)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        res = ds1.merge(fake, join='inner')
        expected = xr.merge([ds1, ds2], join='inner')
        assert_identical(res, expected)
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

def test_merge_custom_dataarray_like_preserve_attrs(monkeypatch):
    orig_DataArray = xr.DataArray
    try:
        ds = xr.Dataset({'a': ((), 0, {'meta': 'x'})})
        ds2 = xr.Dataset({'b': ((), 1, {'meta_b': 'y'})})
        fake = make_fake_da('b', None, ds_return=ds2)
        monkeypatch.setattr(xr, 'DataArray', fake.__class__)
        res = ds.merge(fake)
        assert res['a'].attrs.get('meta') == 'x'
        assert res['b'].attrs.get('meta_b') == 'y'
    finally:
        monkeypatch.setattr(xr, 'DataArray', orig_DataArray)

import xarray.core.dataarray as core_dataarray
import numpy as np
import pytest
import xarray as xr
import xarray.core.dataarray as core_dataarray
from xarray.testing import assert_identical

def test_merge_unnamed_DataArray_monkeypatched_raises_value_error(monkeypatch):
    _monkeypatch_core_DataArray(monkeypatch)
    ds = xr.Dataset({'a': 0})
    da_unnamed = xr.DataArray(2)
    with pytest.raises(ValueError):
        ds.merge(da_unnamed)

import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical
from xarray.core import dtypes
from .test_dataset import create_test_data
from . import raises_regex

def test_merge_dataset_with_monkeypatched_DataArray_named(monkeypatch):
    ds = xr.Dataset({'a': 0})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray(1, name='b')
    result = ds.merge(fake)
    expected = xr.Dataset({'a': 0, 'b': 1})
    assert_identical(result, expected)

def test_merge_dataset_with_monkeypatched_DataArray_unnamed_raises(monkeypatch):
    ds = xr.Dataset({'a': 0})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray(2, name=None)
    with raises_regex(ValueError, 'explicit name'):
        ds.merge(fake)

def test_merge_dataset_with_monkeypatched_DataArray_with_coords(monkeypatch):
    ds = xr.Dataset({'a': ('x', [10])}, coords={'x': [0]})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray([1], name='b', dims=('x',))
    result = ds.merge(fake)
    expected = xr.Dataset({'a': ('x', [10]), 'b': ('x', [1])}, coords={'x': [0]})
    assert_identical(result, expected)

def test_merge_dataset_with_monkeypatched_DataArray_conflict_raises_merge_error(monkeypatch):
    ds = xr.Dataset({'b': 0})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray(1, name='b')
    with pytest.raises(xr.MergeError):
        ds.merge(fake, compat='equals')

def test_merge_dataset_with_monkeypatched_DataArray_no_conflicts_compat_no_conflicts(monkeypatch):
    ds1 = xr.Dataset({'a': ('x', [1, np.nan]), 'x': [0, 1]})

    def to_ds_generator():
        return xr.Dataset({'a': ('x', [np.nan, 2]), 'x': [0, 1]})

    class FakeDA2(FakeDataArray):

        def to_dataset(self):
            return to_ds_generator()
    monkeypatch.setattr(xr, 'DataArray', FakeDA2, raising=False)
    fake = FakeDA2(None, name='a')
    res = ds1.merge(fake, compat='no_conflicts')
    expected = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
    assert_identical(res, expected)

def test_merge_with_monkeypatched_DataArray_join_inner(monkeypatch):
    ds = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)

    class FakeDA3(FakeDataArray):

        def to_dataset(self):
            return xr.Dataset({'b': ('x', [3, 4]), 'x': [1, 2]})
    fake = FakeDA3(None, name='b')
    res = ds.merge(fake, join='inner')
    expected = xr.Dataset({'a': ('x', [2]), 'b': ('x', [3])}, coords={'x': [1]})
    assert_identical(res, expected)

def test_merge_with_monkeypatched_DataArray_fill_value(monkeypatch):
    ds1 = xr.Dataset({'a': ('x', [1, 2]), 'x': [0, 1]})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray(('x', [3, 4]), name='b')

    class FakeDA4(FakeDataArray):

        def to_dataset(self):
            return xr.Dataset({'b': ('x', [3, 4]), 'x': [1, 2]})
    monkeypatch.setattr(xr, 'DataArray', FakeDA4, raising=False)
    fake2 = FakeDA4(None, name='b')
    res = ds1.merge(fake2, fill_value=0)
    expected = xr.Dataset({'a': ('x', [1, 2, 0]), 'b': ('x', [0, 3, 4])}, coords={'x': [0, 1, 2]})
    assert_identical(res, expected)

def test_merge_with_monkeypatched_DataArray_preserve_variable_attrs(monkeypatch):
    ds = xr.Dataset({'a': 0})

    class FakeDA5(FakeDataArray):

        def to_dataset(self):
            return xr.Dataset({'b': ((), 2, {'units': 'm'})})
    monkeypatch.setattr(xr, 'DataArray', FakeDA5, raising=False)
    fake = FakeDA5(None, name='b')
    res = ds.merge(fake)
    assert res['b'].attrs.get('units') == 'm'

def test_merge_with_monkeypatched_DataArray_multiple_calls_restore_symbol(monkeypatch):
    ds = xr.Dataset({'a': 0})
    monkeypatch.setattr(xr, 'DataArray', FakeDataArray, raising=False)
    fake = FakeDataArray(7, name='d')
    res = ds.merge(fake)
    expected = xr.Dataset({'a': 0, 'd': 7})
    assert_identical(res, expected)