import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_selection import VarianceThreshold
from sklearn.utils._testing import assert_array_equal