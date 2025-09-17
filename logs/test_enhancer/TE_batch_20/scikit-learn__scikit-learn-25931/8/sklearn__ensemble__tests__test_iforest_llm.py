from scipy.sparse import csr_matrix
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from scipy.sparse import csr_matrix
from sklearn.utils._testing import assert_array_equal, assert_allclose
pd = pytest.importorskip('pandas')
RNG = check_random_state(0)