import numpy as np
import pytest
from sklearn.utils.testing import assert_array_equal, assert_allclose
from sklearn.cluster.optics_ import OPTICS, compute_optics_graph
from sklearn.metrics.pairwise import pairwise_distances
rng = np.random.RandomState(0)