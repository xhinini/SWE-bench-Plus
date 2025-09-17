import numpy as np
import pytest
from sklearn.utils import check_random_state
from sklearn.ensemble import IsolationForest
from sklearn.utils.testing import assert_array_almost_equal, assert_array_equal, assert_raises, assert_equal
rng = check_random_state(0)