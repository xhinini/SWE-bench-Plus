import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils.testing import assert_equal
rng = check_random_state(0)