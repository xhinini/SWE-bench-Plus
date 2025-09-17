import numpy as np
import pandas as pd
import pytest
from xarray import DataArray
from xarray.core import nanops
from xarray.testing import assert_allclose, assert_equal
from xarray.core.duck_array_ops import nansum