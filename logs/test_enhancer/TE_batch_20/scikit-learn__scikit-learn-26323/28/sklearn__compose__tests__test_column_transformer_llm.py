import pytest
import numpy as np
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator
from sklearn.utils._testing import assert_array_equal
from sklearn.preprocessing import FunctionTransformer