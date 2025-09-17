import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, assert_allclose
RNG = np.random.RandomState(0)