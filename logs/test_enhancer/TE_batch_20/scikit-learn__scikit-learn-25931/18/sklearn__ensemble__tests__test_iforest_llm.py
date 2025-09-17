import pandas as pd
from scipy.sparse import csr_matrix, csc_matrix
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from scipy.sparse import csr_matrix, csc_matrix
from unittest.mock import Mock, patch
from sklearn.ensemble._iforest import _average_path_length
from sklearn.utils._testing import assert_allclose, assert_array_equal
from sklearn.utils._testing import ignore_warnings
pd = pytest.importorskip('pandas')