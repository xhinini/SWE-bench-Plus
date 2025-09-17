import numpy as np
import scipy.sparse as sp
from sklearn.datasets import make_classification
from sklearn.metrics.scorer import get_scorer
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_random_state
from sklearn.linear_model.logistic import _log_reg_scoring_path, LogisticRegression
from sklearn.metrics import log_loss, accuracy_score
import pytest
RNG = check_random_state(0)