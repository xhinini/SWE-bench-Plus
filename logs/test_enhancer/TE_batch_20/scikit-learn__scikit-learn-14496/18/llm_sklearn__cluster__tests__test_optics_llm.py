import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS
from sklearn.metrics.cluster import contingency_matrix
rng = np.random.RandomState(0)