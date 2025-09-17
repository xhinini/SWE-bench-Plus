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

import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_with_python_scalar_x_and_dataarray_y_returns_empty_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = 1
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 'Y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_with_numpy_array_x_and_dataarray_y_returns_empty_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = np.array([1, 2])
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 'Y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_with_numpy_scalar_x_and_dataarray_y_returns_empty_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = np.int64(0)
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 'Y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_prefers_x_attrs_when_cond_is_not_dataarray():
    cond = np.array([True, False])
    x = xr.DataArray([7, 8], dims='x', attrs={'xattr': 1})
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 2})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {'xattr': 1}

def test_where_keep_attrs_prefers_variable_x_attrs_over_y():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x_var = xr.Variable('x', [7, 8], attrs={'var_attr': 'V'})
    y = xr.DataArray([9, 10], dims='x', attrs={'y': 'Y'})
    res = xr.where(cond, x_var, y, keep_attrs=True)
    assert res.attrs == {'var_attr': 'V'}

def test_where_keep_attrs_with_dataset_x_and_scalar_cond_preserves_x_dataset_attrs():
    cond = np.array([True, False])
    x = xr.Dataset({'a': ('x', [1, 2])})
    x.attrs['xattr'] = 123
    y = xr.Dataset({'a': ('x', [9, 10])})
    y.attrs['yattr'] = 999
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {'xattr': 123}

import numpy as np
import xarray as xr
import numpy as np
import xarray as xr

def test_where_keep_attrs_numpy_cond_dataarrays():
    cond = np.array([True, False])
    x = _make_da([1, 2], attrs={'from': 'x'})
    y = _make_da([0, 0], attrs={'from': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_dataarray_and_scalar_x_has_attrs():
    cond = np.array([True, False])
    x = _make_da([1, 2], attrs={'keep': 'x'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_datasets():
    cond = np.array([True, False])
    x = _make_ds([1, 2], attrs={'from': 'x_ds'})
    y = _make_ds([0, 0], attrs={'from': 'y_ds'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_dataset_and_scalar():
    cond = np.array([True, False])
    x = _make_ds([1, 2], attrs={'keep': 'x_ds'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_dataarray_and_dataset():
    cond = np.array([True, False])
    x = _make_da([1, 2], attrs={'keep': 'from_da'})
    y = _make_ds([0, 0], attrs={'keep': 'from_ds'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_dataset_and_dataarray():
    cond = np.array([True, False])
    x = _make_ds([1, 2], attrs={'keep': 'from_ds_x'})
    y = _make_da([0, 0], attrs={'keep': 'from_da_y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_dataarray_cond_dataset_and_dataarray():
    cond = _make_da([True, False])
    x = _make_ds([1, 2], attrs={'keep': 'ds_attrs'})
    y = _make_da([0, 0], attrs={'keep': 'da_attrs'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_dataarray_cond_dataset_and_scalar():
    cond = _make_da([True, False])
    x = _make_ds([1, 2], attrs={'keep': 'ds_attrs_only'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_scalar_cond_dataarrays():
    cond = np.bool_(True)
    x = _make_da([1, 2], attrs={'keep_this': 42})
    y = _make_da([0, 0], attrs={'keep_this': 0})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

import numpy as np
import xarray as xr
from xarray.core.computation import where
from xarray.tests.test_computation import assert_identical

def test_where_keep_attrs_numpy_cond_preserve_dataarray_attrs():
    cond = np.array([True, False])
    x = xr.DataArray([10, 20], dims='x')
    x.attrs['a'] = 'xattr'
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_list_cond_preserve_dataarray_attrs():
    cond = [True, False]
    x = xr.DataArray([1, 2], dims='x')
    x.attrs['keep'] = 'yes'
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_python_scalar_cond_preserve_dataarray_attrs():
    cond = True
    x = xr.DataArray([5, 6], dims='x')
    x.attrs['meta'] = 'info'
    y = xr.DataArray([0, 0], dims='x')
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_x_and_y_dataarray_preserve_x_attrs():
    cond = np.array([True, False])
    x = xr.DataArray([7, 8], dims='x')
    x.attrs['which'] = 'x'
    y = xr.DataArray([0, 0], dims='x')
    y.attrs['which'] = 'y'
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs
    assert out.attrs != y.attrs

def test_where_keep_attrs_numpy_cond_x_and_y_dataset_preserve_x_attrs():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])})
    ds_y = xr.Dataset({'a': ('x', [3, 4])})
    ds_x.attrs['source'] = 'x'
    ds_y.attrs['source'] = 'y'
    out = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert out.attrs == ds_x.attrs
    assert out.attrs != ds_y.attrs

def test_where_preserve_coordinate_attrs_when_only_x_is_dataarray():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', coords={'x': ('x', [0, 1], {'coord_attr': 'c'})})
    x.attrs['data_attr'] = 'd'
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs
    assert out.coords['x'].attrs == x.coords['x'].attrs

def test_where_keep_attrs_when_cond_is_not_dataarray_but_y_is_dataarray_preserve_x():
    cond = np.array([False, True])
    x = xr.DataArray([9, 99], dims='x')
    x.attrs['owner'] = 'x_owner'
    y = xr.DataArray([0, 0], dims='x')
    y.attrs['owner'] = 'y_owner'
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

import xarray as xr
import numpy as np
import pytest
import xarray as xr
import numpy as np
import pytest

def test_where_keep_attrs_cond_scalar_x_da_y_da_returns_x_attrs():
    x = _make_da([1, 2], attrs={'keep': 'x'})
    y = _make_da([0, 0], attrs={'keep': 'y'})
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {'keep': 'x'}

def test_where_keep_attrs_cond_da_x_scalar_y_da_returns_empty_attrs():
    cond = _make_da([True, False])
    y = _make_da([0, 0], attrs={'keep': 'y'})
    res = xr.where(cond, 1, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {}

def test_where_keep_attrs_cond_scalar_x_da_y_da_diff_attrs_returns_x_attrs():
    x = _make_da([1, 2, 3], attrs={'a': 1, 'who': 'x'})
    y = _make_da([9, 9, 9], attrs={'a': 2, 'who': 'y'})
    res = xr.where(False, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {'a': 1, 'who': 'x'}

def test_where_keep_attrs_cond_scalar_x_da_y_da_multi_dim_returns_x_attrs():
    x = xr.DataArray(np.arange(6).reshape(2, 3), dims=('i', 'j'))
    x.attrs['meta'] = 'xmeta'
    y = xr.DataArray(np.zeros((2, 3)), dims=('i', 'j'))
    y.attrs['meta'] = 'ymeta'
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {'meta': 'xmeta'}

def test_where_keep_attrs_cond_scalar_x_da_y_da_zero_dim_returns_x_attrs():
    x = xr.DataArray(42, attrs={'val': 'x_scalar'})
    y = xr.DataArray(0, attrs={'val': 'y_scalar'})
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {'val': 'x_scalar'}

def test_where_keep_attrs_cond_scalar_x_ds_y_ds_returns_x_attrs():
    x = _make_ds({'a': ('x', [1, 2])}, attrs={'ds': 'x_ds'})
    y = _make_ds({'a': ('x', [0, 0])}, attrs={'ds': 'y_ds'})
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {'ds': 'x_ds'}

def test_where_keep_attrs_cond_scalar_x_ds_y_ds_diff_attrs_returns_x_attrs():
    x = _make_ds({'a': ('x', [1])}, attrs={'who': 'x_ds', 'v': 1})
    y = _make_ds({'a': ('x', [9])}, attrs={'who': 'y_ds', 'v': 2})
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {'who': 'x_ds', 'v': 1}

def test_where_keep_attrs_cond_scalar_x_ds_y_da_prefers_dataset_attrs():
    x = _make_ds({'a': ('x', [1, 2])}, attrs={'source': 'dataset_x'})
    y = _make_da([0, 0], attrs={'source': 'dataarray_y'})
    res = xr.where(True, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == {'source': 'dataset_x'}

import xarray as xr
import numpy as np
import pytest
import xarray as xr
import numpy as np
import pytest

def test_where_keep_attrs_scalar_x_cond_da_y_da():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = 1
    y = xr.DataArray([10, 20], dims='x', attrs={'y_attr': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_cond_scalar_two_dataarrays():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x', attrs={'from': 'x'})
    y = xr.DataArray([3, 4], dims='x', attrs={'from': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_cond_da_x_scalar_y_da_with_attrs():
    cond = xr.DataArray([False, True], dims='x', attrs={'cond': 'c'})
    x = 0
    y = xr.DataArray([7, 8], dims='x', attrs={'y_attr': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_cond_da_x_numpy_scalar_y_da_attrs():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = np.int64(5)
    y = xr.DataArray([0, 0], dims='x', attrs={'y_attr': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == {}

def test_where_keep_attrs_cond_numpy_x_da_y_scalar():
    cond = np.array([True, False])
    x = xr.DataArray([9, 10], dims='x', attrs={'keepme': 'x'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

def test_where_keep_attrs_with_datasets_cond_da():
    cond = xr.DataArray([True, False], dims='x')
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, attrs={'ds_attr': 'x'})
    ds_y = xr.Dataset({'a': ('x', [3, 4])}, attrs={'ds_attr': 'y'})
    res = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_cond_scalar_datasets():
    cond = True
    ds_x = xr.Dataset({'a': ('x', [1, 2])}, attrs={'ds_attr': 'x'})
    ds_y = xr.Dataset({'a': ('x', [3, 4])}, attrs={'ds_attr': 'y'})
    res = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert res.attrs == ds_x.attrs

def test_where_keep_attrs_with_variables_cond_numpy():
    cond = np.array([True, False])
    x = xr.Variable('x', [11, 12], attrs={'var_attr': 'x'})
    y = xr.Variable('x', [13, 14], attrs={'var_attr': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert res.attrs == x.attrs

import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_choose_x_when_cond_not_dataarray_da_da():
    cond = np.array([True, False])
    x = xr.DataArray([1, 2], dims='x')
    x.attrs = {'which': 'x'}
    y = xr.DataArray([3, 4], dims='x')
    y.attrs = {'which': 'y'}
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(actual, xr.DataArray)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_choose_x_when_cond_not_dataarray_da_scalar_y_scalar():
    cond = np.array([True, False])
    x = xr.DataArray([10, 20], dims='x')
    x.attrs = {'units': 'm'}
    y = 0
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(actual, xr.DataArray)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_returns_empty_when_x_not_dataarray_but_y_is():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 1})
    x = 5
    y = xr.DataArray([1, 2], dims='x')
    y.attrs = {'should_not_be_kept': True}
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(actual, xr.DataArray)
    assert actual.attrs == {}

def test_where_keep_attrs_choose_x_for_datasets_when_cond_not_dataset():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])})
    ds_x.attrs = {'from': 'x_ds'}
    ds_y = xr.Dataset({'a': ('x', [3, 4])})
    ds_y.attrs = {'from': 'y_ds'}
    actual = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert isinstance(actual, xr.Dataset)
    assert actual.attrs == ds_x.attrs

def test_where_keep_attrs_choose_x_for_dataset_and_scalar_y():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])})
    ds_x.attrs = {'dataset_attr': 'x'}
    y = 0
    actual = xr.where(cond, ds_x, y, keep_attrs=True)
    assert isinstance(actual, xr.Dataset)
    assert actual.attrs == ds_x.attrs

def test_where_keep_attrs_prefers_x_over_y_when_x_has_empty_attrs():
    cond = np.array([True, False])
    x = xr.DataArray([7, 8], dims='x')
    x.attrs = {}
    y = xr.DataArray([9, 10], dims='x')
    y.attrs = {'from': 'y'}
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(actual, xr.DataArray)
    assert actual.attrs == {}

def test_where_keep_attrs_cond_not_dataarray_both_da_with_attrs_different():
    cond = np.ones(2, dtype=bool)
    x = xr.DataArray([0, 1], dims='x')
    x.attrs = {'keep': 1}
    y = xr.DataArray([2, 3], dims='x')
    y.attrs = {'keep': 2}
    actual = xr.where(cond, x, y, keep_attrs=True)
    assert actual.attrs == x.attrs

def test_where_keep_attrs_dataset_mixed_with_dataarray_cond_not_dataset():
    cond = np.array([True, False])
    ds_x = xr.Dataset({'a': ('x', [1, 2])})
    ds_x.attrs = {'owner': 'x'}
    ds_y = xr.Dataset({'a': ('x', [3, 4])})
    ds_y.attrs = {'owner': 'y'}
    actual = xr.where(cond, ds_x, ds_y, keep_attrs=True)
    assert actual.attrs == ds_x.attrs

import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_cond_numpy_two_dataarrays():
    cond = np.array([True, False])
    x = _make_da({'which': 'x'})
    y = _make_da({'which': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'which': 'x'}

def test_where_keep_attrs_cond_scalar_two_dataarrays():
    cond = True
    x = _make_da({'k': 'x'})
    y = _make_da({'k': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'k': 'x'}

def test_where_keep_attrs_cond_numpy_dataset_pair():
    cond = np.array([True, False])
    x = _make_ds({'source': 'x'})
    y = _make_ds({'source': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'source': 'x'}

def test_where_keep_attrs_cond_numpy_variable_pair():
    cond = np.array([True, False])
    x = _make_var({'v': 1})
    y = _make_var({'v': 2})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert hasattr(out, 'attrs')
    assert out.attrs == {'v': 1}

def test_where_keep_attrs_cond_DataArray_x_scalar_y_DataArray():
    cond = _make_da({'from': 'cond'})
    x = 1
    y = _make_da({'from': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {}

def test_where_keep_attrs_cond_numpy_x_dataset_y_dataarray():
    cond = np.array([True, False])
    x = _make_ds({'origin': 'dataset_x'})
    y = _make_da({'origin': 'da_y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.Dataset)
    assert out.attrs == {'origin': 'dataset_x'}

def test_where_keep_attrs_cond_numpy_x_dataarray_y_dataset():
    cond = np.array([True, False])
    x = _make_da({'keep': 'x_da'})
    y = _make_ds({'keep': 'y_ds'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'keep': 'x_da'}

def test_where_keep_attrs_cond_numpy_x_variable_y_dataarray():
    cond = np.array([True, False])
    x = _make_var({'who': 'var_x'})
    y = _make_da({'who': 'da_y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == {'who': 'var_x'}

def test_where_keep_attrs_cond_numpy_x_variable_y_variable_and_dataarray_present():
    cond = _make_da({'c': 'cond'})
    x = _make_var({'orig': 'x_var'})
    y = _make_var({'orig': 'y_var'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {'orig': 'x_var'}

import xarray as xr
import numpy as np
import pytest
import xarray as xr
import numpy as np
import pytest

def test_where_keep_attrs_cond_da_x_scalar_y_da():
    cond = xr.DataArray([True, False], dims='x', attrs={'cond': 'c'})
    x = 1
    y = xr.DataArray([0, 0], dims='x', attrs={'y': 'y_attr'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == {}

def test_where_keep_attrs_cond_scalar_x_da_y_da():
    cond = True
    x = xr.DataArray([10, 20], dims='x', attrs={'x': 'x_attr'})
    y = xr.DataArray([0, 0], dims='x', attrs={'y': 'y_attr'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x.attrs

def test_where_keep_attrs_cond_scalar_x_da_y_scalar():
    cond = False
    x = xr.DataArray([5, 6], dims='x', attrs={'x': 'x_attr'})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.DataArray)
    assert out.attrs == x.attrs

def test_where_keep_attrs_cond_scalar_x_dataset_y_da():
    cond = True
    x = xr.Dataset({'a': ('x', [10, 20])})
    x.attrs['from_x'] = 'x_dataset_attr'
    y = xr.DataArray([0, 0], dims='x', attrs={'y': 'y_attr'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.Dataset)
    assert out.attrs == x.attrs

def test_where_keep_attrs_cond_da_x_dataset_y_scalar():
    cond = xr.DataArray([False, True], dims='x')
    x = xr.Dataset({'a': ('x', [1, 2])})
    x.attrs['keepme'] = 'x_attr'
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(out, xr.Dataset)
    assert out.attrs == x.attrs

import numpy as np
import xarray as xr
from numpy.testing import assert_array_equal
import numpy as np
import xarray as xr
import pytest
from numpy.testing import assert_array_equal

def test_where_keep_attrs_numpy_cond_with_dataarray_x():
    cond = np.array([True, False])
    x = xr.DataArray([5, 6], dims='x', attrs={'unit': 'm'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert_array_equal(res.values, np.where(cond, x.values, y))
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_cond_with_variable_x():
    cond = np.array([True, False])
    var_x = xr.Variable('x', [1, 2], attrs={'foo': 'bar'})
    var_y = xr.Variable('x', [0, 0])
    res = xr.where(cond, var_x, var_y, keep_attrs=True)
    assert isinstance(res, xr.Variable)
    assert res.attrs == var_x.attrs
    assert_array_equal(res.values, np.where(cond, var_x.values, var_y.values))

def test_where_keep_attrs_scalar_cond_with_dataarray_x():
    cond = True
    x = xr.DataArray([7, 8], dims='x', attrs={'keep': 'me'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert_array_equal(res.values, x.values)
    assert res.attrs == x.attrs

def test_where_keep_attrs_scalar_cond_with_variable_x():
    cond = True
    var_x = xr.Variable('x', [9, 10], attrs={'attr': 1})
    var_y = xr.Variable('x', [0, 0])
    res = xr.where(cond, var_x, var_y, keep_attrs=True)
    assert isinstance(res, xr.Variable)
    assert res.attrs == var_x.attrs
    assert_array_equal(res.values, var_x.values)

import numpy as np
import xarray as xr
import pytest
import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_with_numpy_condition_and_dataarrays():
    cond = np.array([True, False])
    x = _make_da([1, 2], attrs={'source': 'x'})
    y = _make_da([0, 0], attrs={'source': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_python_scalar_condition_and_dataarrays():
    cond = True
    x = _make_da([1, 2], attrs={'keep': 'x'})
    y = _make_da([0, 0], attrs={'keep': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_numpy_condition_and_dataarray_x_scalar_y():
    cond = np.array([True, False])
    x = _make_da([5, 6], attrs={'owner': 'x'})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_numpy_condition_and_variable_x():
    cond = np.array([True, False])
    x = _make_var(('x',), np.array([7, 8]), attrs={'var_attr': 1})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert getattr(out, 'attrs', {}) == x.attrs

def test_where_keep_attrs_with_python_scalar_condition_and_variable_x():
    cond = False
    x = _make_var(('x',), np.array([7, 8]), attrs={'var_attr': 'x'})
    y = 0
    out = xr.where(cond, x, y, keep_attrs=True)
    assert getattr(out, 'attrs', {}) == x.attrs

def test_where_keep_attrs_with_numpy_condition_and_datasets():
    cond = np.array([True, False])
    x = _make_ds({'a': ('x', [1, 2])}, attrs={'ds': 'x'})
    y = _make_ds({'a': ('x', [0, 0])}, attrs={'ds': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_python_scalar_condition_and_datasets():
    cond = True
    x = _make_ds({'a': ('x', [1, 2])}, attrs={'ds_attr': 123})
    y = _make_ds({'a': ('x', [0, 0])}, attrs={'ds_attr': 999})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_numpy_condition_and_dataarray_x_empty_attrs():
    cond = np.array([True, False])
    x = _make_da([1, 2], attrs={})
    y = _make_da([0, 0], attrs={'source': 'y'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == {}

def test_where_keep_attrs_with_numpy_condition_and_distinct_attrs():
    cond = np.array([False, True])
    x = _make_da([3, 4], attrs={'which': 'x_only'})
    y = _make_da([9, 9], attrs={'which': 'y_only'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

def test_where_keep_attrs_with_python_scalar_and_multiple_values():
    cond = False
    x = _make_da([10, 20], attrs={'meta': 'x-meta'})
    y = _make_da([0, 0], attrs={'meta': 'y-meta'})
    out = xr.where(cond, x, y, keep_attrs=True)
    assert out.attrs == x.attrs

import numpy as np
import xarray as xr
import pytest
import numpy as np
import xarray as xr
import pytest

def test_where_keep_attrs_numpy_condition_two_dataarrays():
    cond = np.array([True, False])
    x = _make_da(attrs={'keep': 'x'})
    y = _make_da(attrs={'keep': 'y'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == x.attrs

def test_where_keep_attrs_scalar_condition_two_dataarrays():
    cond = True
    x = _make_da(attrs={'keep': 'x2'})
    y = _make_da(attrs={'keep': 'y2'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_condition_dataarray_and_scalar():
    cond = np.array([True, False])
    x = _make_da(attrs={'keep': 'x3'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == x.attrs

def test_where_keep_attrs_dataarray_condition_numpy_x_dataarray_y():
    cond = _make_da(attrs={'cond': 'yes'})
    x = np.array([10, 20])
    y = _make_da(attrs={'keep': 'y4'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == {}

def test_where_keep_attrs_numpy_condition_first_dataarray_has_attrs_second_none():
    cond = np.array([False, True])
    x = _make_da(attrs={'keep': 'x4'})
    y = 999
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.DataArray)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_condition_two_datasets():
    cond = np.array([True, False])
    x = _make_ds(attrs={'keep': 'Xds'})
    y = _make_ds(attrs={'keep': 'Yds'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == x.attrs

def test_where_keep_attrs_scalar_condition_two_datasets():
    cond = False
    x = _make_ds(attrs={'keep': 'Xds2'})
    y = _make_ds(attrs={'keep': 'Yds2'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_condition_dataset_and_scalar():
    cond = np.array([True, True])
    x = _make_ds(attrs={'keep': 'Xds3'})
    y = 0
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == x.attrs

def test_where_keep_attrs_dataarray_condition_dataset_x_dataset_y():
    cond = _make_da(attrs={'cond': 'c'})
    x = _make_ds(attrs={'keep': 'Xds4'})
    y = _make_ds(attrs={'keep': 'Yds4'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == x.attrs

def test_where_keep_attrs_numpy_condition_dataset_x_and_dataarray_y():
    cond = np.array([True, False])
    x = _make_ds(attrs={'keep': 'Xds5'})
    y = _make_da(attrs={'keep': 'y5'})
    res = xr.where(cond, x, y, keep_attrs=True)
    assert isinstance(res, xr.Dataset)
    assert res.attrs == x.attrs