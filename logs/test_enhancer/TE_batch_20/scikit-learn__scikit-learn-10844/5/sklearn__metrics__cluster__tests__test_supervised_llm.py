import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.metrics.cluster import supervised as supervised_module
from sklearn.utils import assert_all_finite
from numpy.testing import assert_allclose