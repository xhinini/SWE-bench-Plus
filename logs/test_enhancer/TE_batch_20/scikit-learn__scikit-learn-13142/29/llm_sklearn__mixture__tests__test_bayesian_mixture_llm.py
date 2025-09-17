import numpy as np
import warnings
import pytest
from numpy.testing import assert_array_equal, assert_allclose
from sklearn.mixture.base import BaseMixture
from sklearn.exceptions import ConvergenceWarning, NotFittedError
X_two = np.array([[0.0], [10.0]])