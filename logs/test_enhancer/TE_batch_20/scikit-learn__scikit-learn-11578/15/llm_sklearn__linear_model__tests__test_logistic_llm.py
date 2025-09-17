from sklearn.metrics.scorer import get_scorer
from sklearn.datasets import make_classification
import numpy as np
import pytest
from sklearn.linear_model.logistic import logistic_regression_path, _log_reg_scoring_path, LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.testing import assert_allclose
from sklearn.metrics.scorer import get_scorer
from sklearn.datasets import make_classification