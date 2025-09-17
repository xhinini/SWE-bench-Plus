import numpy as np
from sklearn.cluster.optics_ import OPTICS
from sklearn.utils.testing import assert_array_equal
from sklearn.utils import shuffle
import pytest
rng = np.random.RandomState(0)