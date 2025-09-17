from sklearn.preprocessing import FunctionTransformer
import numpy as np
import pytest
from numpy.testing import assert_array_equal
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import FunctionTransformer