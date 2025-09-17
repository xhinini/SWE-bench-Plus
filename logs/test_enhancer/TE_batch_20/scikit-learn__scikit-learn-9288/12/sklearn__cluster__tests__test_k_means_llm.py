import numpy as np
from scipy import sparse as sp
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, assert_allclose
RNG = np.random.RandomState(42)
X_blob, _ = make_blobs(n_samples=200, centers=4, n_features=2, random_state=RNG)