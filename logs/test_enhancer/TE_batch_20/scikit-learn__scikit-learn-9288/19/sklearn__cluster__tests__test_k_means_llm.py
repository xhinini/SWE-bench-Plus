import numpy as np
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils import check_random_state
from numpy.testing import assert_array_equal, assert_allclose
RNG = np.random.RandomState(42)
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.5, random_state=RNG)