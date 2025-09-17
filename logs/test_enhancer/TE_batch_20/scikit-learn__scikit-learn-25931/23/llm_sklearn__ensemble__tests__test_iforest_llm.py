import pandas as pd
import numpy as np
import pytest
import warnings
from unittest.mock import Mock, patch
from scipy.sparse import csc_matrix, csr_matrix
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_allclose, assert_array_equal, assert_array_almost_equal
from sklearn.model_selection import train_test_split
pd = pytest.importorskip('pandas')