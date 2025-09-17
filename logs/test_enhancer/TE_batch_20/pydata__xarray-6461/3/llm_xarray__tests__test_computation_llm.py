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