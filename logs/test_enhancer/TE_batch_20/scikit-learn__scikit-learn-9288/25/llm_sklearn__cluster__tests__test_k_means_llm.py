import numpy as np
import scipy.sparse as sp
from sklearn.cluster import KMeans, k_means
from sklearn.datasets import make_blobs
from sklearn.utils.testing import assert_array_equal, assert_allclose, assert_almost_equal
from sklearn.utils.testing import assert_array_almost_equal
import pytest