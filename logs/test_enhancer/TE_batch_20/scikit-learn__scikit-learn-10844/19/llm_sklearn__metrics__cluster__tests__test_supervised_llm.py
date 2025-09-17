import importlib
import numpy as np
from scipy import sparse as sp
from sklearn.metrics.cluster import fowlkes_mallows_score
from numpy.testing import assert_almost_equal