import pytest
import warnings
import numpy as np
from sklearn.utils._testing import assert_array_equal, assert_allclose
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from scipy.sparse import csc_matrix, csr_matrix
from unittest.mock import patch
from sklearn.ensemble._iforest import get_chunk_n_rows as _get_chunk_n_rows