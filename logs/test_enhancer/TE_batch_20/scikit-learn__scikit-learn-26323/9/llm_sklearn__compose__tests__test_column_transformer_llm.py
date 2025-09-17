import numpy as np
import pytest
import pandas as pd
from numpy.testing import assert_array_equal
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import FunctionTransformer
from sklearn.base import BaseEstimator
from sklearn.utils._testing import assert_array_equal as _assert_array_equal