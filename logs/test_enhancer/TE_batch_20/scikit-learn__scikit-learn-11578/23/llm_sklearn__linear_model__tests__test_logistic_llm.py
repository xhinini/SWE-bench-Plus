import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.testing import assert_almost_equal, assert_allclose
from sklearn.utils.testing import assert_array_almost_equal
from sklearn.linear_model.logistic import _log_reg_scoring_path