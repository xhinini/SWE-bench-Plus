import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import pytest
from sklearn.utils.testing import if_safe_multiprocessing_with_blas
from sklearn.utils.testing import assert_array_equal, assert_allclose, assert_almost_equal