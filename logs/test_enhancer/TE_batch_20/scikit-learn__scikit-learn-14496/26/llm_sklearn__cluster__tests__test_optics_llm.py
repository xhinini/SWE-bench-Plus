from sklearn.cluster.optics_ import compute_optics_graph
import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS
from sklearn.metrics import pairwise_distances
from sklearn.utils.testing import assert_allclose