import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal, assert_almost_equal