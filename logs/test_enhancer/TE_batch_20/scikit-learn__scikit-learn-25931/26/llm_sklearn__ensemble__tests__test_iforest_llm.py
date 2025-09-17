import pandas as pd
from scipy.sparse import csc_matrix, csr_matrix
from sklearn.utils import check_random_state
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest
from sklearn.ensemble._iforest import _average_path_length
from sklearn.utils import check_random_state
from scipy.sparse import csc_matrix, csr_matrix
rng = np.random.RandomState(0)