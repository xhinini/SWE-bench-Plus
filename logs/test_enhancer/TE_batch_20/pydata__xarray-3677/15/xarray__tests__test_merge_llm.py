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