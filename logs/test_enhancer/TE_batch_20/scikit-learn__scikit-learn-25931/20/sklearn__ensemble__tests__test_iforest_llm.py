import numpy as np
import pytest
import warnings
from scipy.sparse import csr_matrix, csc_matrix
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_array_equal, assert_allclose
from unittest.mock import patch, Mock