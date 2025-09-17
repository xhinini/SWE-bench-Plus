import numpy as np
import pytest
import warnings
from scipy.sparse import csc_matrix, csr_matrix
pd = pytest.importorskip('pandas')
import numpy as np
import pytest
import warnings
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_allclose, assert_array_equal
from scipy.sparse import csc_matrix, csr_matrix
pd = pytest.importorskip('pandas')
rng = np.random.RandomState(0)