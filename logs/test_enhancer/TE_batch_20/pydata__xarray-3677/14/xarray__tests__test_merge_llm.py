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