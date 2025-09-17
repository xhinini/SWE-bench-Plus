import numpy as np
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.utils.testing import assert_true, assert_false
from sklearn.utils.testing import assert_array_equal, assert_array_almost_equal
from sklearn.utils.testing import assert_raise_message
from sklearn.linear_model.ridge import RidgeClassifierCV