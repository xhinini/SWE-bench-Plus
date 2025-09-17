import numpy as np
from scipy import sparse as sp
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal
from sklearn.utils.testing import assert_allclose
from sklearn.utils.testing import assert_array_almost_equal
RNG = 0
X_blob, _ = make_blobs(n_samples=300, centers=4, n_features=4, random_state=RNG)
X_sparse = sp.csr_matrix(X_blob)