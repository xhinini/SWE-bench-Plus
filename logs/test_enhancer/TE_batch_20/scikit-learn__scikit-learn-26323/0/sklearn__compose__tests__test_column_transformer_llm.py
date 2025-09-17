from collections import UserString
import pytest
import numpy as np
from collections import UserString
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import FunctionTransformer