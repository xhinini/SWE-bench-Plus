from sklearn.utils.testing import assert_array_equal, assert_allclose
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
import numpy as np
import pytest
import numpy as np
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, assert_allclose
import pytest
RNG = 0
X, _ = make_blobs(n_samples=300, centers=5, n_features=2, random_state=RNG)