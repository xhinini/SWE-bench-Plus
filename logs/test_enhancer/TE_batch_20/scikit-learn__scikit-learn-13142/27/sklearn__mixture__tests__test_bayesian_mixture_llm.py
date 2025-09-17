import copy
import numpy as np
import pytest
from sklearn.utils.testing import assert_array_equal
from sklearn.mixture.base import BaseMixture
X = np.array([[0.0], [10.0]])
pytestmark = pytest.mark.filterwarnings('ignore:.*did not converge.*')