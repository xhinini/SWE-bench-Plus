from xarray.core.duck_array_ops import isnull, fillna
import numpy as np
import pytest
from numpy import nan
from numpy.testing import assert_allclose, assert_equal
from xarray.core import nanops
from xarray.core.duck_array_ops import isnull, fillna