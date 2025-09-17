from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression
from sklearn.metrics.scorer import get_scorer
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.testing import assert_almost_equal
import numpy as np
from scipy import sparse
from sklearn.linear_model.logistic import _log_reg_scoring_path
from sklearn.linear_model import LogisticRegression