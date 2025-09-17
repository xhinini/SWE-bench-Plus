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

import numpy as np
import xarray as xr
import pytest
import numpy as np
import xarray as xr
import pytest

def test_non_coarsened_variable_remains_in_position():
    ds = xr.Dataset({'first': ('time', np.arange(24)), 'coarsened': ('time', np.arange(24) + 10), 'static': ('z', np.arange(3)), 'last': (('x', 'time'), np.arange(48).reshape(2, 24))}, coords={'time': np.arange(24), 'x': np.arange(2), 'z': np.arange(3)})
    result = ds.coarsen(time=12, boundary='trim').construct(time=('year', 'month'))
    assert list(result.data_vars.keys()) == list(ds.data_vars.keys())
    assert list(result.data_vars.keys()).index('static') == list(ds.data_vars.keys()).index('static')

def test_multiple_dims_preserve_order_mixed_deps():
    ds = xr.Dataset({'A': ('time', np.arange(24)), 'B': (('y', 'time'), np.arange(48).reshape(2, 24)), 'C': (('x',), np.arange(3)), 'D': (('x', 'time'), np.arange(72).reshape(3, 24))}, coords={'time': np.arange(24), 'x': np.arange(3), 'y': np.arange(2)})
    result = ds.coarsen(time=12, x=3, boundary='trim').construct({'time': ('year', 'month'), 'x': ('x1', 'x2')})
    assert list(result.data_vars.keys()) == list(ds.data_vars.keys())

def test_construct_preserves_order_when_some_vars_unaffected_by_windows():
    ds = xr.Dataset({'v1': ('time', np.arange(24)), 'v2': ('z', np.arange(4)), 'v3': (('time', 'x'), np.arange(240).reshape(24, 10))}, coords={'time': np.arange(24), 'x': np.arange(10), 'z': np.arange(4)})
    result = ds.coarsen(time=12, x=5, boundary='trim').construct({'time': ('year', 'month'), 'x': ('x1', 'x2')})
    assert list(result.data_vars.keys()) == list(ds.data_vars.keys())