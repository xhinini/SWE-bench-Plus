import numpy as np
from sklearn.metrics.cluster import fowlkes_mallows_score, contingency_matrix
from sklearn.utils import assert_all_finite
from sklearn.utils.testing import assert_almost_equal, assert_equal
import math