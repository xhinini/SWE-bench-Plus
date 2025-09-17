import numpy as np
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_allclose
from sklearn.utils.testing import assert_almost_equal
import pytest
RNG = np.random.RandomState(42)
X, _ = make_blobs(n_samples=500, centers=8, n_features=3, random_state=RNG)