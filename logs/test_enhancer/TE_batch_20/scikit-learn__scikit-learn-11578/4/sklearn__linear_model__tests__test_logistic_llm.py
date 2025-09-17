import numpy as np
import scipy.sparse as sp
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics.scorer import get_scorer
from sklearn.metrics import log_loss
from sklearn.linear_model.logistic import _log_reg_scoring_path
from sklearn.linear_model import LogisticRegression
from sklearn.utils import check_random_state
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.testing import assert_allclose, assert_array_almost_equal, assert_array_equal
import pytest
rng = check_random_state(0)