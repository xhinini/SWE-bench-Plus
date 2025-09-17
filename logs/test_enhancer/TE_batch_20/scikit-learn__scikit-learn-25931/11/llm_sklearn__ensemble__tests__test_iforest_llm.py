from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import pytest
from scipy.sparse import csc_matrix, csr_matrix
from unittest.mock import patch, Mock
from sklearn.ensemble import IsolationForest
from sklearn.ensemble._iforest import _average_path_length
from sklearn.utils._testing import assert_array_equal, assert_allclose