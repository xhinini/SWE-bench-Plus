import numpy as np
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, assert_allclose, assert_almost_equal
RNG = np.random.RandomState(0)
X, _ = make_blobs(n_samples=200, centers=4, n_features=4, random_state=RNG)