from sklearn.cluster.optics_ import compute_optics_graph
import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS, compute_optics_graph
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.utils.testing import assert_array_equal, assert_allclose