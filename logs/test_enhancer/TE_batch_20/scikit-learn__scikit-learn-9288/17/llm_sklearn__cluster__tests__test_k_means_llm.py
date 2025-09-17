from sklearn.utils import check_random_state
from sklearn.datasets import make_blobs
import numpy as np
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.utils import check_random_state
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_allclose
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_warns
from sklearn.utils.extmath import row_norms
RNG = np.random.RandomState(0)