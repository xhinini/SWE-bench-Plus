import numpy as np
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.utils._testing import assert_array_equal
from sklearn.feature_selection import VarianceThreshold