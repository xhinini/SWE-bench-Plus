import numpy as np
from sklearn.cluster import KMeans, k_means
from sklearn.utils.testing import assert_array_equal, assert_allclose
from sklearn.utils.testing import if_safe_multiprocessing_with_blas
import numpy as np
import pytest
from sklearn.cluster import KMeans, k_means
from sklearn.utils.testing import assert_array_equal, assert_allclose
from sklearn.utils.testing import if_safe_multiprocessing_with_blas
RNG = np.random.RandomState(0)
X = RNG.normal(size=(200, 5))