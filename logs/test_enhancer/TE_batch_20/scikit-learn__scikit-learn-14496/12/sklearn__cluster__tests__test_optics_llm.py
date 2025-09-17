import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS, compute_optics_graph, cluster_optics_xi
from sklearn.utils.testing import assert_array_equal
rng = np.random.RandomState(42)