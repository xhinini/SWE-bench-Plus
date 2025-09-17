import numpy as np
import pytest
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector
from sklearn.feature_selection import VarianceThreshold
from sklearn.preprocessing import FunctionTransformer
import pandas as pd