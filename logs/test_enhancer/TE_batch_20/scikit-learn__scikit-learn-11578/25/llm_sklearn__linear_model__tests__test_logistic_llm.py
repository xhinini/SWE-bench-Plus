from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.metrics import log_loss
from sklearn.metrics.scorer import get_scorer
from sklearn.linear_model.logistic import _log_reg_scoring_path
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import check_array
import pytest