import numpy as np
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.utils.testing import assert_equal, assert_almost_equal
from sklearn.utils import assert_all_finite