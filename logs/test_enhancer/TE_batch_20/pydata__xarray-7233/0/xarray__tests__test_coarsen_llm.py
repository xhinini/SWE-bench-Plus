pass
import numpy as np
import xarray as xr
import pytest

def test_construct_preserves_data_vars_order():
    ds = xr.Dataset({'a': ('time', np.arange(24)), 'b': ('time', np.arange(24) + 10), 'c': ('time', np.arange(24) + 20)}, coords={'time': np.arange(24), 'static': 1})
    result = ds.coarsen(time=12).construct(time=('year', 'month'))
    assert list(ds.data_vars.keys()) == list(result.data_vars.keys())

def test_construct_preserves_variables_keys_including_coords():
    ds = xr.Dataset({'x': ('time', np.arange(24)), 'y': ('time', np.arange(24) + 100)}, coords={'time': np.arange(24), 'scalar': 5})
    result = ds.coarsen(time=12).construct(time=('year', 'month'))
    assert list(ds.variables.keys()) == list(result.variables.keys())

def test_construct_complex_ordering_with_coords_and_data_vars():
    ds = xr.Dataset()
    ds['a'] = ('time', np.arange(24))
    ds = ds.assign_coords(c1=('time', np.arange(24)))
    ds['b'] = ('time', np.arange(24) + 100)
    ds = ds.assign_coords(c2=('time', np.arange(24) + 200))
    original_variables = list(ds.variables.keys())
    result = ds.coarsen(time=12).construct(time=('year', 'month'))
    assert list(result.variables.keys()) == original_variables