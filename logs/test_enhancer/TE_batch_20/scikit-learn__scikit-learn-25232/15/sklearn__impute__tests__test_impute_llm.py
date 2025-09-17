from sklearn.ensemble import HistGradientBoostingRegressor
import numpy as np
import pytest
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.utils._testing import assert_allclose, assert_array_equal
from sklearn.ensemble import HistGradientBoostingRegressor