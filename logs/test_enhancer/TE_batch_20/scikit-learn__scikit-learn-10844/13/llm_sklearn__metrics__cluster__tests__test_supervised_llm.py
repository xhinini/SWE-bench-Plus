import numpy as np
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.utils.testing import assert_almost_equal, assert_equal
from sklearn.utils import assert_all_finite