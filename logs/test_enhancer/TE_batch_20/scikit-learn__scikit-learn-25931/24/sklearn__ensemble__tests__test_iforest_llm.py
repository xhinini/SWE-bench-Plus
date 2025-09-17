from scipy.sparse import csc_matrix, csr_matrix
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_allclose, assert_array_equal
from scipy.sparse import csc_matrix, csr_matrix