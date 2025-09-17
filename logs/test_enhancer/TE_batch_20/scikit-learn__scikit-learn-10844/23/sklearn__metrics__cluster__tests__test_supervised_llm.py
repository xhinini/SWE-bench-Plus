import numpy as np
from scipy import sparse as sp
import sklearn.metrics.cluster.supervised as _supervised_mod
from sklearn.metrics.cluster import fowlkes_mallows_score
from numpy.testing import assert_almost_equal