import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
import numpy as np
import pandas as pd
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.utils._testing import assert_array_equal
from scipy import sparse