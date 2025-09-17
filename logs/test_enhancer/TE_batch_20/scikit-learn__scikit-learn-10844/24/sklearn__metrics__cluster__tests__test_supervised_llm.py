import numpy as np
from numpy.testing import assert_allclose
from sklearn.metrics.cluster import fowlkes_mallows_score, contingency_matrix
from sklearn.utils import assert_all_finite