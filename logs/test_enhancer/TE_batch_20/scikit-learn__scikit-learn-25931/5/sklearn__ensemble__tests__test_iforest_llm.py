import pandas as pd
from sklearn.exceptions import NotFittedError
from sklearn.utils._testing import assert_allclose
import numpy as np
import pytest
import warnings
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_random_state
from scipy.sparse import csc_matrix