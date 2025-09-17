import numpy as np
import pytest
import xarray as xr
from xarray.testing import assert_identical
from .test_dataset import create_test_data
from . import raises_regex