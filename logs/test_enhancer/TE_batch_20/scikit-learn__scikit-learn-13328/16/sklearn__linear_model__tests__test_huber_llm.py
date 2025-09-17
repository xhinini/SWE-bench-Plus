import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_equal, assert_array_equal
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor