import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.utils._testing import assert_array_equal
from scipy.sparse import csr_matrix, csc_matrix