import pytest
from sklearn.utils import check_random_state
import numpy as np
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils import check_random_state
from sklearn.utils.testing import assert_array_equal, assert_allclose
import pytest
RNG = np.random.RandomState(0)
X, y = make_blobs(n_samples=200, centers=5, n_features=2, random_state=RNG)