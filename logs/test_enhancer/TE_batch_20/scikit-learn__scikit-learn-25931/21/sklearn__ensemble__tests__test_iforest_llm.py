import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils._testing import assert_allclose, assert_array_almost_equal
from sklearn.utils import check_random_state
from scipy.sparse import csc_matrix, csr_matrix