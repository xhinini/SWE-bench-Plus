import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.metrics import log_loss
from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model.logistic import LogisticRegression, logistic_regression_path, _log_reg_scoring_path
from sklearn.preprocessing import LabelEncoder