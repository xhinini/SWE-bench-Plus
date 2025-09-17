import numpy as np
import scipy.sparse as sp
import pytest
from sklearn.utils import check_random_state
from sklearn.metrics import get_scorer
from sklearn.model_selection import StratifiedKFold
from sklearn.datasets import make_classification
from sklearn.linear_model.logistic import _log_reg_scoring_path
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.testing import assert_allclose, assert_array_almost_equal
RNG = check_random_state(0)