import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model.ridge import RidgeClassifierCV, RidgeCV
from sklearn.utils.testing import assert_equal, assert_array_equal, assert_array_almost_equal, assert_raises, assert_raise_message, assert_true