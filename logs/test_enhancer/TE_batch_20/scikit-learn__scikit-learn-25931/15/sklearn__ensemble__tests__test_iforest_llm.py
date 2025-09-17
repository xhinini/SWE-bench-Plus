import pytest
from scipy.sparse import csc_matrix, csr_matrix
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from sklearn.utils._testing import assert_array_almost_equal, assert_array_equal
import pandas as pd
from sklearn.datasets import load_diabetes
diabetes = load_diabetes()