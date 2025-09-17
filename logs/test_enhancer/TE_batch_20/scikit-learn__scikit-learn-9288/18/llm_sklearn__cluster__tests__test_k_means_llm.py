import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.cluster import KMeans
from sklearn.cluster import k_means
from sklearn.datasets import make_blobs
from sklearn.metrics.cluster import v_measure_score
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.utils.testing import assert_almost_equal
from sklearn.utils.testing import assert_warns
from sklearn.utils.testing import assert_raise_message
rng = np.random.RandomState(0)
X_dense, _ = make_blobs(n_samples=300, centers=3, n_features=2, random_state=rng)
X_csr = sp.csr_matrix(X_dense)