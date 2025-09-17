import numpy as np
from sklearn.metrics.cluster import fowlkes_mallows_score, contingency_matrix
from sklearn.utils.testing import assert_almost_equal, assert_all_finite, assert_equal