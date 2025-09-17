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