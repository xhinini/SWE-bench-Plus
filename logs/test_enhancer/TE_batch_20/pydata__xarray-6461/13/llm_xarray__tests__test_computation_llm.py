# No additional imports required beyond numpy and xarray used in the tests.
import numpy as np
import xarray as xr


def test_where_keep_attrs_cond_np_x_da_y_da():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"source": "x"}
    y = xr.DataArray([3, 4], dims="x")
    y.attrs = {"source": "y"}

    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {"source": "x"}


def test_where_keep_attrs_cond_np_x_da_y_scalar():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"meta": "x"}
    y = 0  # scalar
    res = xr.where(cond, x, y, keep_attrs=True)
    # should keep x.attrs even though y is scalar
    assert res.attrs == {"meta": "x"}


def test_where_keep_attrs_cond_np_x_da_y_da_x_has_empty_attrs():
    # ensure that when x has empty attrs we don't accidentally take y's attrs
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {}
    y = xr.DataArray([3, 4], dims="x")
    y.attrs = {"from": "y"}

    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}


def test_where_keep_attrs_cond_da_x_np_y_da_has_attrs():
    # cond is DataArray, x is numpy array, y is DataArray with attrs.
    # keep_attrs should return x.attrs (empty) because x is numpy array (no attrs).
    cond = xr.DataArray([True, False], dims="x")
    x = np.array([1, 2])  # numpy array, no attrs
    y = xr.DataArray([3, 4], dims="x")
    y.attrs = {"should_not_be_taken": True}

    res = xr.where(cond, x, y, keep_attrs=True)
    # x is a plain array -> no attrs -> expect {}
    assert res.attrs == {}


def test_where_keep_attrs_cond_np_x_ds_y_ds():
    # dataset path: cond is numpy, x and y are Datasets with different attrs.
    cond = np.array([True, False])
    x = xr.Dataset({"a": ("x", [1, 2])})
    x.attrs = {"dataset": "x"}
    y = xr.Dataset({"a": ("x", [3, 4])})
    y.attrs = {"dataset": "y"}

    res = xr.where(cond, x, y, keep_attrs=True)
    # should keep attrs from x (the second argument)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {"dataset": "x"}


def test_where_keep_attrs_cond_np_x_ds_y_scalar():
    # cond is numpy, x is Dataset, y is scalar: should keep x.attrs
    cond = np.array([True, False])
    x = xr.Dataset({"a": ("x", [1, 2])})
    x.attrs = {"keep": "x"}
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {"keep": "x"}


def test_where_keep_attrs_cond_da_x_ds_y_ds():
    # cond is DataArray, but x,y are Datasets -> dataset code path should still
    # prefer x.attrs (the second argument)
    cond = xr.DataArray([True, False], dims="x")
    x = xr.Dataset({"a": ("x", [1, 2])})
    x.attrs = {"ds": "x"}
    y = xr.Dataset({"a": ("x", [3, 4])})
    y.attrs = {"ds": "y"}

    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {"ds": "x"}


def test_where_keep_attrs_cond_da_x_ds_y_scalar():
    cond = xr.DataArray([True, False], dims="x")
    x = xr.Dataset({"a": ("x", [1, 2])})
    x.attrs = {"alpha": 1}
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {"alpha": 1}


def test_where_keep_attrs_cond_np_x_var_y_var():
    # Variables: ensure Variable attrs are preserved from x
    cond = np.array([True, False])
    x = xr.Variable(("x",), [1, 2])
    x.attrs = {"var": "x"}
    y = xr.Variable(("x",), [3, 4])
    y.attrs = {"var": "y"}

    res = xr.where(cond, x, y, keep_attrs=True)
    # expect a Variable with x.attrs
    # apply_ufunc/where should return a Variable when Variables passed
    assert isinstance(res, xr.Variable)
    assert res.attrs == {"var": "x"}


def test_where_keep_attrs_cond_np_x_var_y_scalar():
    cond = np.array([True, False])
    x = xr.Variable(("x",), [1, 2])
    x.attrs = {"varattr": 123}
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Variable)
    assert res.attrs == {"varattr": 123}

import numpy as np
import xarray as xr
import pytest
from xarray.tests.test_computation import assert_identical

def test_where_keep_attrs_cond_numpy_x_dataarray_y_scalar():
    x = xr.DataArray([1, 2], dims="x", attrs={"from": "x"})
    cond = np.array([True, False])
    res = xr.where(cond, x, 0, keep_attrs=True)
    assert_identical(res.attrs, x.attrs)

def test_where_keep_attrs_cond_numpy_x_dataarray_y_dataarray():
    x = xr.DataArray([1, 2], dims="x", attrs={"from": "x"})
    y = xr.DataArray([0, 0], dims="x", attrs={"from": "y"})
    cond = np.array([True, False])
    res = xr.where(cond, x, y, keep_attrs=True)
    # should keep attrs of x (second parameter), not y
    assert_identical(res.attrs, x.attrs)
    assert res.attrs != y.attrs

def test_where_keep_attrs_cond_scalar_x_dataarray_y_scalar():
    x = xr.DataArray([1, 2], dims="x", attrs={"keep": "yes"})
    cond = True  # python scalar
    res = xr.where(cond, x, 0, keep_attrs=True)
    assert_identical(res.attrs, x.attrs)

def test_where_keep_attrs_cond_scalar_x_dataarray_y_dataarray():
    x = xr.DataArray([1, 2], dims="x", attrs={"keep": "x"})
    y = xr.DataArray([0, 0], dims="x", attrs={"keep": "y"})
    cond = False  # python scalar
    res = xr.where(cond, x, y, keep_attrs=True)
    # even though cond is scalar and y is a DataArray, keep attrs of x
    assert_identical(res.attrs, x.attrs)

def test_where_keep_attrs_cond_numpy_x_dataset_y_scalar():
    x = xr.Dataset({"a": ("x", [1, 2])}, attrs={"ds_attr": 42})
    cond = np.array([True, False])
    res = xr.where(cond, x, 0, keep_attrs=True)
    # result is a Dataset and should keep dataset-level attrs from x
    assert_identical(res.attrs, x.attrs)

def test_where_keep_attrs_cond_numpy_x_dataset_y_dataset():
    x = xr.Dataset({"a": ("x", [1, 2])}, attrs={"which": "x"})
    y = xr.Dataset({"a": ("x", [0, 0])}, attrs={"which": "y"})
    cond = np.array([True, False])
    res = xr.where(cond, x, y, keep_attrs=True)
    # should keep attrs of x (second parameter), not y
    assert_identical(res.attrs, x.attrs)
    assert res.attrs != y.attrs

def test_where_keep_attrs_x_has_no_attrs_returns_empty():
    x = xr.DataArray([1, 2], dims="x")  # no attrs
    y = xr.DataArray([0, 0], dims="x", attrs={"y": "meta"})
    cond = np.array([True, False])
    res = xr.where(cond, x, y, keep_attrs=True)
    # x has no attrs, so result.attrs should be empty dict
    assert_identical(res.attrs, {})

def test_where_keep_attrs_cond_dataarray_x_dataarray_y_dataset():
    cond = xr.DataArray([True, False], dims="x")
    x = xr.DataArray([1, 2], dims="x", attrs={"keep": "x"})
    y = xr.Dataset({"a": ("x", [0, 0])}, attrs={"which": "y"})
    res = xr.where(cond, x, y, keep_attrs=True)
    # keep attrs of x (the second argument) even if y is a Dataset
    assert_identical(res.attrs, x.attrs)

def test_where_keep_attrs_with_variable_as_x():
    # x is a Variable with attrs; result should be a Variable and keep attrs
    x_var = xr.Variable("x", [1, 2], attrs={"v": 1})
    cond = np.array([True, False])
    res = xr.where(cond, x_var, 0, keep_attrs=True)
    # result is a Variable - compare attrs
    assert_identical(res.attrs, x_var.attrs)

def test_where_keep_attrs_prefers_second_argument_over_later_dataarrays():
    # cond is non-xarray, x is DataArray (attrs A), y is DataArray (attrs B).
    # Ensure keep_attrs=True chooses x.attrs, not y.attrs.
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x", attrs={"chosen": "x"})
    y = xr.DataArray([0, 0], dims="x", attrs={"chosen": "y"})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert_identical(res.attrs, x.attrs)
    assert res.attrs != y.attrs

import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_numpy_cond_two_dataarrays():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'x'})
    y = xr.DataArray([0, 0], dims='x', attrs={'keep': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_scalar_cond_two_dataarrays():
    cond = True
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'x'})
    y = xr.DataArray([0, 0], dims='x', attrs={'keep': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_dataarray_and_scalar():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'x'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_two_datasets():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, coords={'x': [0, 1]})
    ds_x.attrs['keep'] = 'x'
    ds_y = xr.Dataset({'a': ('x', [0, 0])}, coords={'x': [0, 1]})
    ds_y.attrs['keep'] = 'y'
    res = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_numpy_cond_dataset_and_scalar():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, coords={'x': [0, 1]})
    ds_x.attrs['keep'] = 'x'
    res = xr.where(cond, ds_x, 0, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_numpy_cond_two_variables():
    cond = np.array([True, False])
    var_x = xr.Variable(('x',), [1, 2])
    var_x.attrs['keep'] = 'x'
    var_y = xr.Variable(('x',), [0, 0])
    var_y.attrs['keep'] = 'y'
    res = xr.where(cond, var_x, var_y, keep_attrs=True)
    assert getattr(res, 'attrs', {}) == var_x.attrs

def test_where_keep_attrs_numpy_cond_variable_and_scalar():
    cond = np.array([True, False])
    var_x = xr.Variable(('x',), [1, 2])
    var_x.attrs['keep'] = 'x'
    res = xr.where(cond, var_x, 0, keep_attrs=True)
    assert getattr(res, 'attrs', {}) == var_x.attrs

def test_where_keep_attrs_numpy_cond_dataarray_and_variable():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'x'})
    y = xr.Variable(('x',), [0, 0])
    y.attrs['keep'] = 'y'
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_not_dataarray_only_x_is_dataarray():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'x'})
    y = 0.0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

import numpy as np
import xarray as xr
import numpy as np
import xarray as xr

def test_where_keep_attrs_dataarray_with_scalar_y():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"a": "xattr"}
    y = 0
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataarray_with_numpy_y():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"a": "xattr"}
    y = np.array([0, 0])
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataarray_with_variable_y():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"a": "xattr"}
    y = xr.Variable("x", [0, 0])
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataarray_with_list_y():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"a": "xattr"}
    y = [0, 0]
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataarray_with_dataarray_y():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x")
    x.attrs = {"a": "xattr"}
    y = xr.DataArray([0, 0], dims="x")
    y.attrs = {"b": "yattr"}
    actual = xr.where(cond, x, y, keep_attrs=True)
    # keep_attrs=True should preserve x.attrs (not y.attrs)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataset_with_scalar_y():
    cond = np.array([True, False])
    x = xr.Dataset({"v": ("x", [1, 2])})
    x.attrs = {"ds": "xattrs"}
    y = 0
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataset_with_dataset_y():
    cond = np.array([True, False])
    x = xr.Dataset({"v": ("x", [1, 2])})
    x.attrs = {"ds": "xattrs"}
    y = xr.Dataset({"v": ("x", [0, 0])})
    y.attrs = {"ds": "yattrs"}
    actual = xr.where(cond, x, y, keep_attrs=True)
    # keep_attrs=True should preserve x.attrs (not y.attrs)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_variable_with_scalar_y():
    cond = np.array([True, False])
    x = xr.Variable("x", [1, 2])
    x.attrs = {"var": "xattrs"}
    y = 0
    actual = xr.where(cond, x, y, keep_attrs=True)
    # returns a Variable; its attrs should be preserved from x
    assert getattr(actual, "attrs", {}) == x.attrs

def test_where_keep_attrs_variable_with_numpy_y():
    cond = np.array([True, False])
    x = xr.Variable("x", [1, 2])
    x.attrs = {"var": "xattrs"}
    y = np.array([0, 0])
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert getattr(actual, "attrs", {}) == x.attrs

def test_where_keep_attrs_dataset_with_variable_y():
    cond = np.array([True, False])
    x = xr.Dataset({"v": ("x", [1, 2])})
    x.attrs = {"ds": "xattrs"}
    y = xr.Variable("x", [0, 0])
    actual = xr.where(cond, x, y, keep_attrs=True)
    # keep_attrs=True should preserve x.attrs even when other args include Variables
    assert actual.attrs == x.attrs

# No additional imports required beyond pytest, numpy, xarray used in test_code.
import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_cond_scalar_dataarray():
    # cond is a Python scalar, x is a DataArray with attrs -> attrs should be kept
    x = xr.DataArray([1, 2], dims="x", attrs={"keep": "x"})
    res = xr.where(True, x, 0, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_numpy_array_dataarray():
    # cond is a numpy array, x is a DataArray with attrs -> attrs should be kept
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims="x", attrs={"keep": "x2"})
    res = xr.where(cond, x, 0, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_scalar_dataset():
    # cond is scalar, x is a Dataset with attrs -> dataset attrs should be kept
    ds = xr.Dataset({"a": ("x", [1, 2])}, attrs={"ds_attr": "keep_ds"})
    res = xr.where(True, ds, 0, keep_attrs=True)
    assert res.attrs == ds.attrs

def test_where_keep_attrs_cond_scalar_x_and_y_dataarray():
    # cond is scalar, both x and y are DataArray with different attrs
    # keep_attrs should keep x.attrs (the second argument), not y.attrs
    x = xr.DataArray([1, 2], dims="x", attrs={"which": "x_attr"})
    y = xr.DataArray([0, 0], dims="x", attrs={"which": "y_attr"})
    res = xr.where(True, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_numpy_x_and_y_datasets():
    # cond is numpy array, both x and y are Datasets with different attrs
    cond = np.array([True, False])
    x = xr.Dataset({"a": ("x", [1, 2])}, attrs={"keep": "ds_x"})
    y = xr.Dataset({"a": ("x", [0, 0])}, attrs={"keep": "ds_y"})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_scalar_variable():
    # cond scalar, x is a Variable with attrs -> attrs should be kept on result
    x = xr.Variable("x", [1, 2], attrs={"vattr": "keep_var"})
    res = xr.where(True, x, 0, keep_attrs=True)
    # result for Variable input is a Variable; it should carry attrs
    assert getattr(res, "attrs", {}) == x.attrs

def test_where_keep_attrs_cond_numpy_two_variables():
    # cond numpy array, x and y are Variables with different attrs
    # keep_attrs should keep attrs of x (the second argument)
    cond = np.array([True, False])
    x = xr.Variable("x", [1, 2], attrs={"v": "xvar"})
    y = xr.Variable("x", [0, 0], attrs={"v": "yvar"})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert getattr(res, "attrs", {}) == x.attrs

def test_where_keep_attrs_cond_dataarray_two_variables():
    # cond is a DataArray, x and y are Variables
    # _all_of_type will pick up Variables; keep_attrs should keep x.attrs
    cond = xr.DataArray([True, False], dims="x")
    x = xr.Variable("x", [1, 2], attrs={"v": "xvar2"})
    y = xr.Variable("x", [0, 0], attrs={"v": "yvar2"})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert getattr(res, "attrs", {}) == x.attrs

def test_where_keep_attrs_cond_numpy_both_dataarrays():
    # cond numpy array, both x and y DataArray: should keep x.attrs
    cond = np.array([True, False, True])
    x = xr.DataArray([1, 2, 3], dims="x", attrs={"keepme": "x"})
    y = xr.DataArray([0, 0, 0], dims="x", attrs={"keepme": "y"})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

import numpy as np
import xarray as xr
import pytest

def test_where_cond_da_x_scalar_y_da_keeps_no_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = 5
    y = xr.DataArray([10, 20], dims='x', attrs={'y': 'Y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == {}

def test_where_cond_scalar_x_da_y_da_keeps_x_attrs():
    cond = True
    x = xr.DataArray([1, 2], dims='x', attrs={'keep': 'X'})
    y = xr.DataArray([3, 4], dims='x', attrs={'keep': 'Y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x.attrs

def test_where_cond_da_x_numpy_y_da_keeps_no_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = np.array([7, 8])
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 'Y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == {}

def test_where_cond_da_x_variable_y_da_keeps_variable_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x_var = xr.Variable(('x',), [2, 4], attrs={'var_attr': 'V'})
    y = xr.DataArray([0, 1], dims='x', attrs={'y': 'Y'})
    out = xr.where(cond, x_var, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x_var.attrs

def test_where_cond_scalar_x_variable_y_da_keeps_variable_attrs():
    cond = False
    x_var = xr.Variable(('x',), [5, 6], attrs={'var_attr': 'V2'})
    y = xr.DataArray([1, 2], dims='x', attrs={'y': 'Y'})
    out = xr.where(cond, x_var, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x_var.attrs

def test_where_cond_scalar_x_dataset_y_da_keeps_x_dataset_attrs():
    cond = True
    x_ds = xr.Dataset({'a': ('x', [2, 3])}, coords={'x': [0, 1]})
    x_ds.attrs = {'which': 'XDS2'}
    y = xr.DataArray([9, 9], dims='x', attrs={'y': 'Y'})
    out = xr.where(cond, x_ds, y, keep_attrs=True)
    assert isinstance(out, xr.Dataset)
    assert out.attrs == x_ds.attrs

def test_where_cond_scalar_x_da_y_scalar_keeps_x_attrs():
    cond = True
    x = xr.DataArray([3, 4], dims='x', attrs={'keepme': 'Xonly'})
    y = -1
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x.attrs

import numpy as np
import xarray as xr
import pytest
import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_cond_scalar_x_da_y_da():
    cond = True
    x = make_da([1, 2], attrs={'xa': 1})
    y = make_da([0, 0], attrs={'ya': 2})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'xa': 1}

def test_where_keep_attrs_cond_scalar_x_da_y_scalar():
    cond = True
    x = make_da([1, 2], attrs={'xa': 1})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'xa': 1}

def test_where_keep_attrs_cond_numpy_x_da_y_da():
    cond = np.array([True, False])
    x = make_da([1, 2], attrs={'xa': 10})
    y = make_da([9, 9], attrs={'ya': 20})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'xa': 10}

def test_where_keep_attrs_cond_scalar_x_ds_y_ds():
    cond = True
    x = make_ds(attrs={'xds': 'A'})
    y = make_ds(attrs={'yds': 'B'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'xds': 'A'}

def test_where_keep_attrs_cond_numpy_x_ds_y_ds():
    cond = np.array([True, True])
    x = make_ds(attrs={'xds': 'A'})
    y = make_ds(attrs={'yds': 'B'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'xds': 'A'}

def test_where_keep_attrs_cond_scalar_x_var_y_var():
    cond = True
    x = make_var(attrs={'xv': 1})
    y = make_var(attrs={'yv': 2})
    out = xr.where(cond, x, y, keep_attrs=True)
    if hasattr(out, 'attrs'):
        assert out.attrs == {'xv': 1}
    else:
        pytest.skip('Returned plain array (no attrs) - environment dependent')

def test_where_keep_attrs_cond_numpy_x_var_y_scalar():
    cond = np.array([True, False])
    x = make_var(attrs={'xv': 'keepme'})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    if hasattr(out, 'attrs'):
        assert out.attrs == {'xv': 'keepme'}
    else:
        pytest.skip('Returned plain array (no attrs) - environment dependent')

def test_where_keep_attrs_cond_scalar_x_da_empty_y_da_has_attrs():
    cond = True
    x = make_da([1, 2], attrs={})
    y = make_da([0, 0], attrs={'ya': 'should_not_be_chosen'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {}

def test_where_keep_attrs_cond_numpy_x_ds_empty_y_ds_has_attrs():
    cond = np.array([True, False])
    x = make_ds(attrs={})
    y = make_ds(attrs={'yds': 'wrong'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {}

import xarray as xr
import numpy as np
import pytest

def test_where_keep_attrs_cond_da_x_scalar_y_da():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = 0
    y = xr.DataArray([10, 20], dims='x', attrs={'y': 'bad'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_cond_scalar_x_da_y_da():
    cond = True
    x = xr.DataArray([1, 2], dims='x', attrs={'x': 'good'})
    y = xr.DataArray([3, 4], dims='x', attrs={'y': 'bad'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_da_x_ndarray_y_da():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = np.array([0, 0])
    y = xr.DataArray([10, 20], dims='x', attrs={'y': 'bad'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_cond_scalar_x_dataset_y_dataset():
    cond = True
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, attrs={'ds': 'x_attr'})
    ds_y = xr.Dataset({'a': ('x', [3, 4])}, attrs={'ds': 'y_attr'})
    res = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_cond_da_x_dataset_y_scalar():
    cond = xr.DataArray([True, False], dims='x')
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, attrs={'ds': 'x_attr'})
    y = 0
    res = xr.where(cond, ds_x, y, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_cond_scalar_x_da_y_dataset():
    cond = True
    x = xr.DataArray([1, 2], dims='x', attrs={'x': 'good'})
    ds_y = xr.Dataset({'a': ('x', [3, 4])}, attrs={'ds': 'y_attr'})
    res = xr.where(cond, x, ds_y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_da_x_ndarray_y_da_coords():
    cond = xr.DataArray([True, False], dims='x')
    x = np.array([1, 2])
    y = xr.DataArray([3, 4], dims='x', coords={'x': ('x', [0, 1], {'coord': 'bad'})}, attrs={'y': 'bad'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}
    assert res.attrs == {}

def test_where_keep_attrs_with_mixed_argument_positions():
    cond = xr.DataArray([True, False], dims='x')
    x = xr.DataArray([1, 2], dims='x', attrs={'chosen': 'x'})
    y = xr.Dataset({'a': ('x', [3, 4])}, attrs={'ds': 'y_attr'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs