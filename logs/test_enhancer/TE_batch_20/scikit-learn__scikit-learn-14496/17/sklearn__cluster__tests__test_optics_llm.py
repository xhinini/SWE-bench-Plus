import numpy as np
import pytest
from sklearn.cluster.optics_ import OPTICS, compute_optics_graph
from sklearn.utils.testing import assert_array_equal
from sklearn.utils import shuffle