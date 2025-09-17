import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor, LinearRegression
from sklearn.utils.testing import assert_array_almost_equal, assert_almost_equal
import pytest