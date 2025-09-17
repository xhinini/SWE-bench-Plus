import numpy as np
import copy
import pytest
from sklearn.mixture.base import BaseMixture
from sklearn.utils import check_random_state
from sklearn.utils.testing import assert_array_equal
rng = np.random.RandomState(0)
X_small = rng.randn(10, 2)
X_large = rng.randn(50, 3)