import numpy as np
import pytest
import pandas as pd
from xarray import Dataset, DataArray, combine_by_coords
from xarray.testing import assert_identical, assert_equal